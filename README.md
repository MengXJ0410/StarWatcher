# 🌟 StarWatcher - 星空观测时间查询工具

This is a simple small-scale project — a lightweight software I built and completed using Python with the assistance of GitHub Copilot, designed specifically for querying the observation times of stars.

一个轻量级的星空观测时间查询工具，使用 Python 和 Streamlit 构建，帮助天文爱好者找到最佳观测时间。

## ✨ 功能特点

- 🎯 **智能查询**：根据地点和目标天体推荐最佳观测时间
- 📊 **数据可视化**：直观展示观测质量、可见度等指标
- 🌤️ **天气考量**：结合天气条件和月相给出专业建议
- 📅 **日期范围**：支持多日期范围查询
- 🎨 **友好界面**：使用 Streamlit 构建的现代化 Web 界面

## 🚀 快速开始

### 本地运行

1. **克隆仓库**
   ```bash
   git clone https://github.com/MengXJ0410/StarWatcher.git
   cd StarWatcher
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **运行应用**
   ```bash
   streamlit run app.py
   ```

4. **访问应用**
   
   在浏览器中打开 `http://localhost:8501`

## 🌐 部署到 GitHub

### 部署到 Streamlit Community Cloud

1. **Fork 或克隆此仓库到你的 GitHub 账号**

2. **访问 [Streamlit Community Cloud](https://streamlit.io/cloud)**

3. **点击 "New app"**

4. **填写部署信息**：
   - Repository: `你的用户名/StarWatcher`
   - Branch: `main` 或 `copilot/adjust-date-column-width`
   - Main file path: `app.py`

5. **点击 "Deploy"**

6. **等待部署完成**，应用将自动启动

### 使用 GitHub Actions 自动部署（可选）

可以创建 `.github/workflows/deploy.yml` 文件来实现自动化部署：

```yaml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Test app can start
      run: |
        streamlit --version
```

## 📋 项目结构

```
StarWatcher/
├── app.py                 # 主应用文件
├── requirements.txt       # Python 依赖
├── .streamlit/
│   └── config.toml       # Streamlit 配置
└── README.md             # 项目说明
```

## 💡 使用说明

1. 在左侧边栏输入观测参数：
   - 观测地点
   - 目标天体
   - 日期范围
   - 天气质量要求
   - 月相要求

2. 点击 "🔍 查询观测时间" 按钮

3. 查看结果页面：
   - 📅 **日期**：观测日期（使用加权列宽，显示完整）
   - ⭐ **观测质量**：综合评分
   - 👁️ **可见度**：能见度百分比
   - ⏰ **最佳时段**：推荐的观测时间窗口
   - **建议**：根据综合条件给出的观测建议

## 🛠️ 技术栈

- **Python 3.9+**
- **Streamlit**: Web 应用框架
- **datetime**: 日期时间处理
- **math**: 数学计算

## 📝 开发说明

### 列宽调整

应用中的结果展示使用了加权列宽设置：

```python
# 使用加权列宽而非等宽列
col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
```

这样设置可以：
- 为"日期"列（col1）分配更多空间，避免日期被截断
- 为"推荐"信息（col4）分配更多空间，完整显示建议文本
- 保持中间的"观测质量"和"可见度"列紧凑

### 自定义配置

可以在 `.streamlit/config.toml` 中修改主题颜色和其他配置。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 👤 作者

Built with ❤️ using Python, Streamlit & GitHub Copilot

---

🌟 如果这个项目对你有帮助，请给一个 Star！
