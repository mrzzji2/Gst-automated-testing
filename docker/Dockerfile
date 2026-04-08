# Web Automation Test Framework Dockerfile
# 用于在 Docker 容器中运行自动化测试

FROM python:3.11-slim

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    DEBIAN_FRONTEND=noninteractive

# 设置工作目录
WORKDIR /app

# 安装系统依赖和 Playwright 浏览器依赖
RUN apt-get update && apt-get install -y \
    # 基础工具
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    # 清理
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt requirements-dev.txt ./

# 安装 Python 依赖
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install -r requirements-dev.txt

# 安装 Playwright 浏览器
RUN playwright install --with-deps chromium
# 可选：安装其他浏览器
# RUN playwright install --with-deps firefox
# RUN playwright install --with-deps webkit

# 复制项目文件
COPY . .

# 创建必要的目录
RUN mkdir -p reports/html reports/allure reports/junit reports/screenshots reports/videos logs/auto

# 设置权限
RUN chmod +x jenkins/scripts/*.sh || true

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import playwright; print('OK')" || exit 1

# 默认命令
CMD ["pytest", "tests/", "-v", "--browser=chromium", "--headless=true"]
