# 🎫 景区门票余量监控工具

实时监控景区门票余量，当检测到有余票时通过 Telegram 推送通知。

## 功能特点

- ✅ 定时检查指定日期的门票余量
- ✅ 支持监控多个日期和场次（日场/夜场）
- ✅ 支持命令行指定日期（单个、多个、日期范围）
- ✅ 有余票时自动发送 Telegram 通知
- ✅ 避免重复通知同一条信息
- ✅ 支持 Docker 容器化部署

## 快速开始

### 本地运行

```bash
cd ticket-monitor
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 单次检查
python monitor.py --once

# 持续监控
python monitor.py
```

### Docker 运行

```bash
# 构建镜像
docker build -t ticket-monitor .

# 运行容器
docker run -d --name ticket-monitor \
  -v $(pwd)/config.json:/app/config.json:ro \
  -e TZ=Asia/Shanghai \
  ticket-monitor

# 或使用 docker-compose
docker-compose up -d
```

## 命令行参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `-d, --dates` | 指定监控日期 | `-d 2025-12-07` |
| `-i, --interval` | 检查间隔(秒) | `-i 60` |
| `--once` | 只运行一次 | `--once` |
| `-c, --config` | 配置文件路径 | `-c config.json` |

### 日期格式支持

```bash
# 单个日期
python monitor.py -d 2025-12-07

# 多个日期（逗号分隔）
python monitor.py -d "2025-12-07,2025-12-08,2025-12-09"

# 日期范围（波浪号）
python monitor.py -d "2025-12-07~2025-12-15"

# 混合使用
python monitor.py -d "2025-12-07,2025-12-10~2025-12-15"
```

## 配置文件

编辑 `config.json`：

```json
{
  "telegram": {
    "bot_token": "你的Bot Token",
    "chat_id": "你的Chat ID"
  },
  "monitor": {
    "interval_seconds": 30,
    "target_dates": ["2025-12-07", "2025-12-08"],
    "target_sessions": ["日场", "夜场"]
  }
}
```

### 获取 Telegram Bot 配置

1. 在 Telegram 中搜索 `@BotFather`
2. 发送 `/newbot` 创建机器人
3. 复制获得的 Bot Token
4. 发送消息给你的 Bot，然后访问 `https://api.telegram.org/bot<TOKEN>/getUpdates` 获取 Chat ID

### 更新认证信息

当 Cookie/Token 过期时，需要重新抓包更新 `config.json` 中的 `headers` 字段。

## 环境变量（Docker）

| 变量 | 说明 |
|------|------|
| `TG_BOT_TOKEN` | Telegram Bot Token |
| `TG_CHAT_ID` | Telegram Chat ID |
| `MONITOR_INTERVAL` | 检查间隔(秒) |
| `TARGET_DATES` | 监控日期(逗号分隔) |

## 注意事项

⚠️ **Token 有效期**：登录 Token 通常有时效，过期后需要重新登录抓包获取新的认证信息。

⚠️ **请求频率**：不要设置过短的间隔（建议不低于30秒），避免被服务器限制。
