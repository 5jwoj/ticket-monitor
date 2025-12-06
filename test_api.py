#!/usr/bin/env python3
"""
测试脚本：分析景区门票API接口（处理压缩响应）
"""

import requests
import json

# 用户提供的请求头
headers = {
    "Host": "wap.lotsmall.cn",
    "Cookie": "ssxmod_itna=1-Yq0x0DuQD=e4yDfxeKYKitTiODRD9lQhBgxBP018D_xQ5508D6QDB441aeHOcwyRP4t_70ip3pY0MxD/iGeGzDidKGhDBWE7=Q0d_vXrm0jRG5HiUDhxIHW0W=koa7RI68SU5Ds=ugcLLmP3xGnDD3EDB=DCTqxdxGGDDtoxG==DDeDtRiDf_Eo6QTDb8rDKwIb7GoK3Ede3o4Rz_GdFYhs3xhdQY_PzDhciSYzkY448G5HaUdD88gUS8h3Qond2jfexA=oxAtDATqDmqDF0jWWT8oD6diYK0wzZGGuWUvs48AzAN9dUBv5QGYQG7E34YD; ssxmod_itna2=1-Yq0x0DuQD=e4yDfxeKYKitTiODRD9lQhBgxBP018D_xQ5508D6QDB441aeHOcwyRP4t_70ip3pYW4iTpQWRonANs_jyXGqMrB2WXKeD; tr_de_id=ZHYtU1JZSUtUR0tMWkNV; tr_se_id=c2UtRlhUWVlKUk1RS0VP; SERVERCORSID=14799a1b7de57723e3899dc089a978c0|1764988351|1764988323; SERVERID=14799a1b7de57723e3899dc089a978c0|1764988351|1764988323; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219aed67a5e4ff8-0ff3b58d851787-63487c08-400760-19aed67a5e5faa%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTlhZWQ2N2E1ZTRmZjgtMGZmM2I1OGQ4NTE3ODctNjM0ODdjMDgtNDAwNzYwLTE5YWVkNjdhNWU1ZmFhIiwiJGlkZW50aXR5X21lcmNoYW50SW5mb19pZCI6IjI1MzA0In0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2219aed67a5e4ff8-0ff3b58d851787-63487c08-400760-19aed67a5e5faa%22%7D; sensorsdata2015jssdksession=%7B%22session_id%22%3A%2219af15c7a40398708e95e0ad0df9f858617e7540076019af15c7a413f7a%22%2C%22first_session_time%22%3A1764985961023%2C%22latest_session_time%22%3A1764988350178%7D; m_id=25304; leaguerInfoId=944337064945674531; leaguerInfoId_25304=944337064945674531; token=eyJhbGciOiJIUzUxMiJ9.eyJ1IjoiOTQ0MzM3MDY0OTQ1Njc0NTMxIiwidCI6IjAiLCJleHAiOjE3NjQ5OTU1MjZ9.WI_vo6XfdPVXH9DiKtggePaIf0vdmPMpGp3XRKiWx1Su_eJskIqMQRyWbU5WmqCdFpQm7UVOB4iY3KPjwnn0Cw; token_25304=eyJhbGciOiJIUzUxMiJ9.eyJ1IjoiOTQ0MzM3MDY0OTQ1Njc0NTMxIiwidCI6IjAiLCJleHAiOjE3NjQ5OTU1MjZ9.WI_vo6XfdPVXH9DiKtggePaIf0vdmPMpGp3XRKiWx1Su_eJskIqMQRyWbU5WmqCdFpQm7UVOB4iY3KPjwnn0Cw; connect.sid=s%3AiDS_HKyr97Wfqqp0VDEOO2Q_9d6fA2be.nfJtVs6Vdp4INHT%2BAdXJVRCIdGOvxWQjaY9fhcVOhyM; acw_tc=ac11000117649883241126352e00655cbb3455c516213f0a01085e598c7576; tr_wb_id=d2ItVU5STlpYV1ZQQ1ha; aliyungf_tc=36d593bfc249ebbd89d53423adcbb23cc59ba8816d6d8525c012bf8c18dc511e; SESSIONID=5f5f1f65-4501-4604-ae55-76fabaacb9fd",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.66(0x18004228) NetType/WIFI Language/zh_CN",
    "Referer": "https://wap.lotsmall.cn/vue/detail/ticket?id=85184&m_id=25304&productId=994808&skuCode=MP2025113019362385264",
    "merLang": "CN",
    "Origin": "https://wap.lotsmall.cn",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh-Hans;q=0.9",
    # 不要求压缩，让requests自动处理
    # "Accept-Encoding": "gzip, deflate, br",
    "access-token": "eyJhbGciOiJIUzUxMiJ9.eyJ1IjoiOTQ0MzM3MDY0OTQ1Njc0NTMxIiwidCI6IjAiLCJleHAiOjE3NjQ5OTU1MjZ9.WI_vo6XfdPVXH9DiKtggePaIf0vdmPMpGp3XRKiWx1Su_eJskIqMQRyWbU5WmqCdFpQm7UVOB4iY3KPjwnn0Cw",
}

# 票务参数
ticket_params = {
    "id": "85184",
    "m_id": "25304",
    "productId": "994808",
    "skuCode": "MP2025113019362385264"
}

# 测试可能的API端点
api_endpoints = [
    # 产品详情
    f"https://wap.lotsmall.cn/merapi/product/detail?productId={ticket_params['productId']}&m_id={ticket_params['m_id']}",
    f"https://wap.lotsmall.cn/merapi/ticket/detail?id={ticket_params['id']}&m_id={ticket_params['m_id']}",
    # 库存/日历/SKU
    f"https://wap.lotsmall.cn/merapi/sku/calendar?productId={ticket_params['productId']}&m_id={ticket_params['m_id']}",
    f"https://wap.lotsmall.cn/merapi/ticket/sku/list?productId={ticket_params['productId']}&m_id={ticket_params['m_id']}",
    f"https://wap.lotsmall.cn/merapi/product/sku/list?productId={ticket_params['productId']}&m_id={ticket_params['m_id']}",
]

print("=" * 60)
print("测试景区门票API接口")
print("=" * 60)

session = requests.Session()

for endpoint in api_endpoints:
    print(f"\n{'='*60}")
    print(f"尝试: {endpoint}")
    try:
        resp = session.get(endpoint, headers=headers, timeout=10)
        print(f"状态码: {resp.status_code}")
        print(f"Content-Type: {resp.headers.get('Content-Type', 'N/A')}")
        print(f"Content-Encoding: {resp.headers.get('Content-Encoding', 'N/A')}")
        if resp.status_code == 200:
            try:
                data = resp.json()
                print(f"\n响应 JSON:")
                print(json.dumps(data, ensure_ascii=False, indent=2)[:2000])
                if len(json.dumps(data)) > 2000:
                    print("... (响应已截断)")
            except Exception as e:
                print(f"JSON解析失败: {e}")
                print(f"响应(文本前500字符): {resp.text[:500]}")
        else:
            print(f"响应: {resp.text[:300]}")
    except Exception as e:
        print(f"错误: {e}")
