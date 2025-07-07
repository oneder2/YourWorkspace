# YourWorkspace

个人工作间与职业锚点项目 - 一个基于Flask和Svelte的个人工作空间应用

## 线上地址 (Live Demo)

🎉 **应用已成功部署，您可以通过以下地址访问：**
[https://oneder2.pythonanywhere.com/](https://oneder2.pythonanywhere.com/)

## 项目概述
#### 个人工作间与职业锚点 (Personal Workspace & Career Anchor)

YourWorkspace旨在为用户提供一个私人的、动态的在线空间，作为其个人的“职业锚点”。它不仅用于对外专业展示，更核心的是帮助用户清晰认知 **“我做过什么，做得怎么样 (What I've done & how well I did it)”，“我正在做什么 (What I'm doing currently)”，以及“我打算做什么 (What I plan to do in the future)”**。通过结构化反思、职业发展追踪和目标管理，助力用户保持前进的动力。

#### 🚀 主要功能模块

项目围绕用户的职业发展时间轴和核心自我认知构建，主要包含以下模块：

1.  **身份锚点 (My Anchor / Profile):**
    * 用户定义和展示核心身份信息的空间，包括：个人简介、核心技能、价值观、职业使命等。
    * 这是整个工作间的基石，是其他模块信息的出发点和归宿。

2.  **正在做 (Doing):**
    * **智能待办事项 (Smart Todo List):** 管理当前的任务和行动项。
    * **当前焦点 (Current Focus):** 从待办事项中精选出1-3个最需要集中精力处理的任务，突出显示。

3.  **已做 (Done):**
    * **成就记录 (Achievements):** 系统记录和展示用户已完成的重要项目、取得的成就和习得的经验。

4.  **打算做 (Future Plans):**
    * **未来规划 (Future Plans):** 用户设定中长期目标、展望未来发展方向的空间。
    * 强调计划的“可见性”和“重要性”，鼓励将长远规划分解为可行动的步骤，但避免日常待办的紧迫感。

## 🎯 功能特性

### 已实现功能
- ✅ 用户认证（注册/登录）
- ✅ 个人档案管理（Anchor页面）
- ✅ 任务管理（Doing页面）
- ✅ 成就跟踪（Done页面）
- ✅ 计划制定（Plan页面）
- ✅ 响应式设计
- ✅ 深色模式
- ✅ 自定义背景

### 原始设想功能
- 📝 博客系统集成
- 🤖 AI生成任务报告
- 📊 月报/年报生成
- 🔗 社交平台同步

## 🎯 核心用户群体

主要面向希望有效管理个人职业发展、进行自我反思、展示专业价值的：

* 知识工作者
* 自由职业者
* 学生
* 任何希望提升个人组织和规划能力的人

## 📈 项目状态：MVP开发中
* Phase 1 阶段已完成
* ✅ **已成功部署至PythonAnywhere**
* 正在开展Phase 2阶段开发
* 更多项目规划详见 `项目开发基本方针.txt`

---

***以下是具体实现及技术部分***

## 🛠️ 技术栈 (Tech Stack)

* **前端 (Frontend):**
    * 框架: SvelteKit
    * 样式: Tailwind CSS
    * 状态管理: Svelte Stores
* **后端 (Backend):**
    * 框架: Flask (Python)
    * API: RESTful API
    * 用户认证: JWT
* **数据库 (Database):**
    * SQLite
* **未来集成 (Future Integration):**
    * 大型语言模型 (LLM) API (如 OpenAI, Google Gemini) 用于智能分析与内容生成。

## 📝 设计理念与原则

* **用户中心 (User-Centric):** 始终以用户的需求和体验为核心。
* **专注与简化 (Focus & Simplification):** 界面设计力求清晰直观，避免信息过载，帮助用户聚焦核心任务。
* **模块化与解耦 (Modularity & Decoupling):** 各功能模块既独立又互相关联，易于维护和扩展。
* **平衡规划与行动 (Balancing Vision & Action):** 特别是在“打算做”模块，致力于在远期规划的激励性和可行动性之间找到平衡。
* **专业且激励人心 (Professional & Inspiring):** 视觉和交互设计旨在营造专业、可信赖且能激发用户积极性的氛围。

## 🚀 快速开始 (本地开发)

### 先决条件
- Git
- Node.js & npm

### 手动部署（推荐用于开发）

#### 后端服务
详细说明请参考 **[后端README](backend/README.md)**

```bash
cd backend
pip install -r requirements.txt
source venv/bin/activate
python run.py
```

#### 前端应用
详细说明请参考 **[前端README](svelte@latest/README.md)**

```bash
cd svelte@latest
npm install
npm run dev
```

## 部署 (Deployment)

本项目支持多种部署方式。对于线上生产环境，推荐使用 PaaS 平台或 Docker。

### PythonAnywhere 部署指南 (PaaS - 已验证)

本项目已成功部署在 PythonAnywhere 上。这是一个高性价比且对 Flask/Python 项目非常友好的平台。以下是部署步骤：

**阶段一：一次性SSH密钥设置**

1.  在 PythonAnywhere 的 Bash 控制台生成 SSH 密钥 (`ssh-keygen -t ed25519`)。
2.  将公钥 (`~/.ssh/id_ed25519.pub`) 添加到您的 GitHub 账户的 "SSH and GPG keys" 设置中。

**阶段二：部署流程**

1.  **克隆仓库**: 在 PythonAnywhere Bash 控制台使用 SSH 地址克隆您的项目。
    ```bash
    git clone git@github.com:YourUserName/YourWorkspace.git
    ```
2.  **进入后端目录**: 所有后续操作都在 `backend` 目录内进行。
    ```bash
    cd ~/YourWorkspace/backend
    ```
3.  **上传 `.env` 文件**: 通过 PythonAnywhere 的 "Files" 页面，将您本地的 `.env` 文件上传到当前的 `backend` 目录中。
4.  **创建虚拟环境**:
    ```bash
    python3.10 -m venv venv  # (请使用您希望的Python版本)
    ```
5.  **安装依赖**:
    ```bash
    source venv/bin/activate
    pip install -r requirements.txt
    ```
6.  **创建数据库**: 首先创建 `instance` 目录，然后运行数据库迁移。
    ```bash
    mkdir instance
    flask db upgrade head
    ```
7.  **配置Web应用**: 前往 PythonAnywhere 的 "Web" 标签页进行设置：
    * **Source code**: `/home/YourUserName/YourWorkspace/backend`
    * **Virtualenv**: `/home/YourUserName/YourWorkspace/backend/venv`
    * **WSGI file**: 点击并编辑，确保其中的 `project_path` 变量正确指向您的 `backend` 目录。
    * **Static files**: 添加一条映射：
        * URL: `/`
        * Directory: `/home/YourUserName/YourWorkspace/backend/static`
8.  **重新加载**: 点击绿色的 **"Reload"** 按钮。您的应用现已上线！

## ⚠️ 重要提醒

**本项目为AI生产力主导开发**，在进行人工修改前请务必阅读 **[开发须知](DEVELOPMENT.md)**

## 🧪 测试

### 后端测试
```bash
cd backend
poetry run pytest
```

### 前端测试
```bash
cd svelte@latest
npm run check      # 类型检查
npm run build      # 构建测试
```

## 📦 部署选项

| 部署方式 | 适用场景 | 状态 | 文档链接 |
|---|---|---|---|
| 手动部署 | 本地开发 | ✅ 已验证 | [快速开始](#-快速开始-本地开发) |
| PythonAnywhere (PaaS) | 线上生产/爱好项目 | ✅ 已验证 | [PythonAnywhere 部署指南](#pythonanywhere-部署指南-paas---已验证) |
| Docker Compose | 生产环境 | 🚧 开发中 | [Docker部署指南](DOCKER.md) |


## 🤝 贡献指南

1.  **阅读文档** - 首先阅读 [开发须知](DEVELOPMENT.md)
2.  **理解架构** - 本项目为AI主导开发，请保持架构一致性
3.  **遵循规范** - 参考各模块README中的代码规范
4.  **测试验证** - 确保修改不破坏现有功能
5.  **更新文档** - 及时更新相关文档

## 📄 许可证

MIT License

## 📞 支持

如需帮助，请参考：
- [开发须知](DEVELOP.md) - 详细的开发指南
- [后端README](backend/README.md) - 后端服务文档
- [前端README](svelte@latest/README.md) - 前端应用文档
- [Docker部署指南](DOCKER.md) - 容器化部署说明
- [PythonAnywhere 部署指南](#pythonanywhere-部署指南-paas---已验证) - 线上部署说明