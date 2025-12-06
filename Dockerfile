FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY monitor.py .
COPY config.json .

# 环境变量（可选覆盖配置）
ENV TG_BOT_TOKEN=""
ENV TG_CHAT_ID=""
ENV MONITOR_INTERVAL=""
ENV TARGET_DATES=""

# 默认运行监控
CMD ["python", "monitor.py"]
