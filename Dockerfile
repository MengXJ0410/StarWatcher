# 使用官方轻量级 Python 镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 1. 先复制依赖文件 (利用 Docker 缓存加速构建)
COPY requirements.txt .

# 2. 安装依赖 (使用清华源加速，防止超时)
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 3. 复制项目所有代码
COPY . .

# 4. 暴露 Streamlit 默认端口
EXPOSE 8501

# 5. 启动命令
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
