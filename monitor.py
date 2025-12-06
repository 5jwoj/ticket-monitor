#!/usr/bin/env python3
"""
景区门票余量监控工具
监控指定日期的门票余量，有余票时通过 Telegram 推送通知
"""

import json
import time
import requests
from datetime import datetime, timedelta
from urllib.parse import urlencode
import logging
import os

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class TicketMonitor:
    """门票余量监控器"""
    
    API_URL = "https://wap.lotsmall.cn/bff/product/api/product/timeReserveList"
    
    def __init__(self, config_path: str = "config.json"):
        """初始化监控器"""
        self.config = self._load_config(config_path)
        self.session = requests.Session()
        self.last_notified = {}  # 记录已通知的状态，避免重复通知
        
    def _load_config(self, config_path: str) -> dict:
        """加载配置文件"""
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 支持环境变量覆盖配置
        if os.environ.get('TG_BOT_TOKEN'):
            config['telegram']['bot_token'] = os.environ['TG_BOT_TOKEN']
        if os.environ.get('TG_CHAT_ID'):
            config['telegram']['chat_id'] = os.environ['TG_CHAT_ID']
        if os.environ.get('MONITOR_INTERVAL'):
            config['monitor']['interval_seconds'] = int(os.environ['MONITOR_INTERVAL'])
        if os.environ.get('TARGET_DATES'):
            config['monitor']['target_dates'] = os.environ['TARGET_DATES'].split(',')
            
        return config
    
    def _get_headers(self) -> dict:
        """构建请求头"""
        return {
            "Host": "wap.lotsmall.cn",
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.66(0x18004228) NetType/WIFI Language/zh_CN",
            "Referer": self.config["ticket"]["url"],
            "Origin": "https://wap.lotsmall.cn",
            "merLang": "CN",
            "Cookie": self.config["headers"]["Cookie"],
            "access-token": self.config["headers"]["access-token"],
            "sk": self.config["headers"]["sk"],
            "sign": self.config["headers"]["sign"],
        }
    
    def _get_timestamp(self) -> str:
        """获取时间戳"""
        return str(int(time.time() * 1000))
    
    def check_stock(self, date: str) -> list:
        """
        检查指定日期的库存
        
        Args:
            date: 日期，格式 YYYY-MM-DD
            
        Returns:
            包含场次库存信息的列表
        """
        payload = {
            "alternate": "T",
            "startTime": date,
            "endTime": date,
            "externalCode": self.config["ticket"]["external_code"],
            "merchantId": self.config["ticket"]["merchant_id"],
            "merchantInfoId": self.config["ticket"]["merchant_id"],
            "modelCode": self.config["ticket"]["model_code"],
            "xj_time_stamp_2019_11_28": self._get_timestamp(),
        }
        
        try:
            response = self.session.post(
                self.API_URL,
                headers=self._get_headers(),
                data=urlencode(payload),
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get("status") == 200:
                return result.get("data", [])
            else:
                logger.warning(f"API返回异常状态: {result}")
                return []
                
        except requests.RequestException as e:
            logger.error(f"请求失败: {e}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {e}")
            return []
    
    def send_telegram(self, message: str) -> bool:
        """
        发送 Telegram 通知
        
        Args:
            message: 消息内容
            
        Returns:
            是否发送成功
        """
        bot_token = self.config["telegram"]["bot_token"]
        chat_id = self.config["telegram"]["chat_id"]
        
        if bot_token == "YOUR_BOT_TOKEN_HERE" or chat_id == "YOUR_CHAT_ID_HERE":
            logger.warning("Telegram未配置，跳过通知")
            print(f"\n📢 通知内容:\n{message}")
            return False
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                logger.info("Telegram 通知发送成功")
                return True
            else:
                logger.error(f"Telegram 通知发送失败: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Telegram 通知异常: {e}")
            return False
    
    def format_notification(self, date: str, available_sessions: list) -> str:
        """格式化通知消息"""
        msg = f"🎫 <b>门票有余票啦！</b>\n\n"
        msg += f"📅 日期: {date}\n"
        msg += f"🎟️ 可预约场次:\n"
        
        for session in available_sessions:
            msg += f"  • {session['name']}: {session['num']}张\n"
            msg += f"    时段: {session['startTime']}-{session['endTime']}\n"
        
        msg += f"\n🔗 <a href='{self.config['ticket']['url']}'>立即预约</a>"
        return msg
    
    def run_once(self, target_dates: list = None) -> dict:
        """
        执行一次检查
        
        Args:
            target_dates: 指定检查的日期列表，为None时使用配置文件中的日期
            
        Returns:
            各日期的库存状态
        """
        results = {}
        dates_to_check = target_dates or self.config["monitor"]["target_dates"]
        target_sessions = self.config["monitor"].get("target_sessions", [])
        
        for date in dates_to_check:
            stocks = self.check_stock(date)
            available = []
            
            for stock in stocks:
                # 检查是否有余票
                if stock.get("num", 0) > 0:
                    # 如果指定了场次，只关注指定场次
                    if target_sessions and stock.get("name") not in target_sessions:
                        continue
                    available.append(stock)
            
            results[date] = {
                "all_stocks": stocks,
                "available": available
            }
            
            # 如果有余票，发送通知
            if available:
                notify_key = f"{date}_{[s['name'] for s in available]}"
                if notify_key not in self.last_notified:
                    message = self.format_notification(date, available)
                    self.send_telegram(message)
                    self.last_notified[notify_key] = datetime.now()
                    logger.info(f"🎉 {date} 有余票: {[s['name'] for s in available]}")
            else:
                logger.info(f"📭 {date} 暂无余票")
        
        return results
    
    def run(self, target_dates: list = None):
        """
        持续运行监控
        
        Args:
            target_dates: 指定检查的日期列表，为None时使用配置文件中的日期
        """
        interval = self.config["monitor"]["interval_seconds"]
        dates_to_check = target_dates or self.config["monitor"]["target_dates"]
        
        logger.info(f"🚀 开始监控，间隔 {interval} 秒")
        logger.info(f"📅 监控日期: {dates_to_check}")
        
        while True:
            try:
                logger.info("-" * 40)
                self.run_once(dates_to_check)
                logger.info(f"⏳ 等待 {interval} 秒后继续检查...")
                time.sleep(interval)
            except KeyboardInterrupt:
                logger.info("👋 监控已停止")
                break
            except Exception as e:
                logger.error(f"监控异常: {e}")
                time.sleep(interval)


def parse_dates(date_str: str) -> list:
    """
    解析日期参数，支持多种格式：
    - 单个日期: 2025-12-07
    - 多个日期: 2025-12-07,2025-12-08
    - 日期范围: 2025-12-07~2025-12-10
    """
    dates = []
    
    for part in date_str.split(','):
        part = part.strip()
        if '~' in part:
            # 日期范围
            start, end = part.split('~')
            start_date = datetime.strptime(start.strip(), '%Y-%m-%d')
            end_date = datetime.strptime(end.strip(), '%Y-%m-%d')
            current = start_date
            while current <= end_date:
                dates.append(current.strftime('%Y-%m-%d'))
                current += timedelta(days=1)
        else:
            dates.append(part)
    
    return dates


def main():
    """主入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="景区门票余量监控工具")
    parser.add_argument("-c", "--config", default="config.json", help="配置文件路径")
    parser.add_argument("--once", action="store_true", help="只运行一次")
    parser.add_argument("-d", "--dates", type=str, help="指定监控日期，支持: 单个日期(2025-12-07)、多个日期(2025-12-07,2025-12-08)、日期范围(2025-12-07~2025-12-10)")
    parser.add_argument("-i", "--interval", type=int, help="检查间隔(秒)，覆盖配置文件")
    args = parser.parse_args()
    
    monitor = TicketMonitor(args.config)
    
    # 解析指定日期
    target_dates = None
    if args.dates:
        target_dates = parse_dates(args.dates)
        print(f"📅 指定监控日期: {target_dates}")
    
    # 覆盖检查间隔
    if args.interval:
        monitor.config["monitor"]["interval_seconds"] = args.interval
    
    if args.once:
        results = monitor.run_once(target_dates)
        print("\n📊 检查结果:")
        for date, data in results.items():
            print(f"\n{date}:")
            for stock in data["all_stocks"]:
                status = "✅ 有票" if stock.get("num", 0) > 0 else "❌ 售罄"
                print(f"  {stock.get('name', 'N/A')}: {status} ({stock.get('num', 0)}张)")
    else:
        monitor.run(target_dates)


if __name__ == "__main__":
    main()
