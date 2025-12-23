# StarWatcher (星空观测助手) 🔭

StarWatcher 是一个轻量级的，我借助Copliot开发的星空观测辅助工具，它可以根据你所在的城市，计算出木星、火星、月亮等天体的最佳观测时间。
本项目由 Python 构建，并使用了 GitHub Copilot 辅助开发。


本项目由阿里云ESA提供加速、计算和保护![阿里云ESA Pages](
https://img.alicdn.com/imgextra/i3/O1CN01H1UU3i1Cti9lYtFrs_!!6000000000139-2-tps-7534-844.png)


## ✨ 功能特点

- **多模式支持**：提供 Web 界面 (基于 Streamlit) 和 命令行 (CLI) 两种使用方式。
- **精准计算**：基于 `ephem` 天文库，精确计算天体的升起和落下时间。
- **智能推荐**：自动判断观测时段是否在夜间，给出观测推荐星级。
- **支持天体**：木星 (Jupiter)、火星 (Mars)、月亮 (Moon)、土星 (Saturn)、金星 (Venus)。
- **支持城市**：杭州、上海、北京、深圳、广州 (支持扩展)。

## 🛠️ 安装指南

1. **克隆项目**
   ```bash
   git clone https://github.com/MengXJ0410/StarWatcher.git
   cd StarWatcher
   ```

2. **安装依赖**
   建议使用 Python 3.8+ 环境：
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 使用方法![Uploading O1CN01H1UU3i1Cti9lYtFrs_!!6000000000139-2-tps-7534-844.png…]()


### 方式一：Web 界面 (推荐)
启动 Streamlit 网页应用，获得可视化的交互体验：
```bash
streamlit run app.py
```
运行后浏览器会自动打开，你可以在侧边栏选择城市和目标天体进行查询。

### 方式二：命令行工具
如果你喜欢简洁的终端操作，可以直接运行脚本：
```bash
python starwatcher.py
```
根据提示输入城市名 (如 `Hangzhou`) 和天体名称即可。

## 🧰 技术栈

- **Python**: 核心编程语言
- **Streamlit**: Web 应用框架
- **Ephem**: 高精度天文计算库
- **Pytz**: 时区处理

## 🤝 贡献
欢迎提交 Issue 或 Pull Request 来完善这个小工具！
