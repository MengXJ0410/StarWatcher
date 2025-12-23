# StarWatcher (星空观测助手) 🔭

StarWatcher 是一个运行在边缘端 (Edge) 的星空观测辅助工具。它利用 WebAssembly 技术，让 Python 代码直接在你的浏览器中运行，无需后端服务器即可计算木星、火星、月亮等天体的最佳观测时间。

本项目核心逻辑由 Python 构建，借助 GitHub Copilot 辅助开发，并针对边缘计算环境进行了轻量化重构。

> 本项目由阿里云 ESA (Edge Security Acceleration) 提供全球边缘加速与计算支持。

![阿里云ESA Pages](https://img.alicdn.com/imgextra/i3/O1CN01H1UU3i1Cti9lYtFrs_!!6000000000139-2-tps-7534-844.png)

## 📸 应用预览

| 观测报告 | 移动端适配 |
| :---: | :---: |
| ![展示1](https://github.com/MengXJ0410/StarWatcher/blob/main/display1.png?raw=true) | ![展示2](https://github.com/MengXJ0410/StarWatcher/blob/main/display2.png?raw=true) |

## ✨ 功能特点

- **⚡️ 边缘计算 (Edge Native)**：Web 版本基于 `stlite` 技术，将 Python 运行时打包为 WebAssembly，实现了 **"Serverless"** 甚至是 **"Server-free"** 的极致部署体验。
- **📱 多模式支持**：
  - **Web 端**：即开即用，无需安装，支持 PWA。
  - **CLI 端**：保留了基于 `ephem` 库的高精度命令行工具。
- **🔭 智能推荐**：根据地理位置计算天体升落时间，自动过滤白天的无效观测时段，给出观测推荐星级。
- **🪐 支持天体**：木星 (Jupiter)、火星 (Mars)、月亮 (Moon)、土星 (Saturn)、金星 (Venus)。
- **🏙️ 支持城市**：杭州、上海、北京、深圳、广州 (支持扩展)。

## 🛠️ 本地开发与安装


# StarWatcher 项目部署指南

## 1. 安装依赖
```bash
pip install -r requirements.txt
```

## 2. 运行 Web 应用
```bash
streamlit run app.py
```

## 3. 运行命令行工具
```bash
python starwatcher.py
```

## ☁️ 阿里云 ESA 部署指南 (重点)

本项目已针对 **阿里云 ESA (Edge Security Acceleration) Pages** 进行了深度优化。请按照以下配置进行部署：

### 准备文件
确保仓库中包含以下核心文件：
- `index.html` (Stlite 引导入口)
- `app.py` (纯 Python 业务逻辑，不能包含 ephem 等 C 扩展库)

### ESA 控制台配置
在 ESA Pages 创建项目时，请严格使用以下配置，以确保静态资源被正确抓取：

| 配置项 | 填写内容 | 说明 |
|--------|----------|------|
| 框架预设 | None / Static | 纯静态站点模式 |
| 构建命令 | `mkdir -p dist && cp index.html app.py dist/` | 手动将核心文件复制到发布目录 |
| 静态资源目录 | `dist` | 告诉 ESA 发布该目录下的文件 |
| 安装命令 | (留空) | 不需要 pip install |
| 函数入口 | (留空) | 不需要 Serverless 函数 |

## 🧰 技术栈
- **Python 3**: 核心逻辑
- **Streamlit**: UI 框架
- **Stlite (Pyodide)**: Python on WebAssembly 运行时
- **Aliyun ESA**: 边缘托管与分发网络

---

**注意**：部署到阿里云 ESA 时，请确保 `app.py` 文件中不包含任何 C 扩展库的依赖，因为这些库无法在 WebAssembly 环境中正常运行。
