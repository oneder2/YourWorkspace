# YourWorkplace

个人工作间与职业锚点项目 - 一个基于Flask和Svelte的个人工作空间应用

## 项目概述

YourWorkplace是一个个人工作空间应用，用于管理任务、成就和未来计划。它提供了一种结构化的方式来反思您的职业旅程并跟踪您的进展。

## 功能特点

- **Done页面**: 跟踪您的成就和已完成的任务
- **Doing页面**: 管理您当前的任务和重点关注领域
- **Plan页面**: 规划您的未来目标和项目
- **Anchor页面**: 您的专业档案和身份

## 技术栈

- **前端**: Svelte 5 with SvelteKit, Tailwind CSS
- **后端**: Flask (Python) with SQLite数据库
- **认证**: 基于JWT的身份验证

## 先决条件

- Docker和Docker Compose
- Git

## 📚 文档导航

本项目提供了详细的文档系统，请根据您的需求选择相应的文档：

- **[后端服务操作指南](backend/README.md)** - Flask后端API的详细使用说明
- **[前端应用开发指南](svelte@latest/README.md)** - Svelte前端应用的开发和构建说明
- **[开发须知](DEVELOPMENT.md)** - 详细的开发规范和注意事项（⚠️ AI主导项目）
- **[Docker部署指南](DOCKER.md)** - 容器化部署的完整说明

## 🚀 快速开始

### 使用Docker Compose（推荐用于生产）

1. 克隆仓库:
   ```bash
   git clone <repository-url>
   cd YourWorkplace
   ```

2. 在根目录创建`.env`文件:
   ```bash
   cp .env.example .env
   # 编辑.env文件设置您的密钥
   ```

3. 启动应用:
   ```bash
   chmod +x deploy.sh
   ./deploy.sh start
   ```

4. 访问应用: http://localhost

### 手动部署（推荐用于开发）

#### 后端服务

详细说明请参考 **[后端README](backend/README.md)**

```bash
cd backend
poetry install
poetry run python init_db.py
poetry run python run.py
```

#### 前端应用

详细说明请参考 **[前端README](svelte@latest/README.md)**

```bash
cd svelte@latest
npm install
npm run dev
```

## ⚠️ 重要提醒

**本项目为AI生产力主导开发**，在进行人工修改前请务必阅读 **[开发须知](DEVELOPMENT.md)**

## 🏗️ 项目架构

### 后端 (Flask)
- RESTful API设计
- JWT认证系统
- SQLite数据库
- Poetry依赖管理

### 前端 (Svelte 5)
- 现代化SPA应用
- Tailwind CSS样式
- 响应式设计
- 深色模式支持

详细的架构说明请参考各模块的README文档。

## 🧪 测试

### 后端测试
```bash
cd backend
poetry run pytest
poetry run python test_api.py  # API集成测试
```

### 前端测试
```bash
cd svelte@latest
npm run check      # 类型检查
npm run build      # 构建测试
```

## 📦 部署选项

| 部署方式 | 适用场景 | 文档链接 |
|---------|---------|---------|
| Docker Compose | 生产环境 | [Docker部署指南](DOCKER.md) |
| 手动部署 | 开发环境 | [后端README](backend/README.md) + [前端README](svelte@latest/README.md) |

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

## 🤝 贡献指南

1. **阅读文档** - 首先阅读 [开发须知](DEVELOPMENT.md)
2. **理解架构** - 本项目为AI主导开发，请保持架构一致性
3. **遵循规范** - 参考各模块README中的代码规范
4. **测试验证** - 确保修改不破坏现有功能
5. **更新文档** - 及时更新相关文档

## 📄 许可证

MIT License

## 📞 支持

如需帮助，请参考：
- [开发须知](DEVELOPMENT.md) - 详细的开发指南
- [Docker部署指南](DOCKER.md) - 容器化部署说明
- [后端README](backend/README.md) - 后端服务文档
- [前端README](svelte@latest/README.md) - 前端应用文档

---

**🤖 本项目由AI助手主导开发，体现了AI在现代软件开发中的强大能力**
=======
# 个人工作间与职业锚点 (Personal Workspace & Career Anchor)

本项目旨在为用户提供一个私人的、动态的在线空间，作为其个人的“职业锚点”。它不仅用于对外专业展示，更核心的是帮助用户清晰认知 **“我做过什么，做得怎么样 (What I've done & how well I did it)”，“我正在做什么 (What I'm doing currently)”，以及“我打算做什么 (What I plan to do in the future)”**。通过结构化反思、职业发展追踪和目标管理，助力用户保持前进的动力。

## ✨ 项目愿景与核心目标

在快节奏的现代职场中，清晰的自我认知和有效的职业规划至关重要。本项目致力于成为每位用户值得信赖的数字化伙伴，提供一个：

* **个性化的职业档案库：** 系统记录个人成就、技能、经历与成长。
* **动态的自我反思平台：** 辅助用户梳理当前状态，明确未来方向。
* **智能的行动管理助手：** 连接长期愿景与短期目标，将规划付诸实践。
* **(未来) AI赋能的洞察引擎：** 基于用户数据提供个性化建议与周期性报告，深化职业发展洞察。

## 🎯 核心用户群体

主要面向希望有效管理个人职业发展、进行自我反思、展示专业价值的：

* 知识工作者
* 自由职业者
* 学生
* 任何希望提升个人组织和规划能力的人

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

## 🛠️ 技术栈 (Tech Stack)

* **前端 (Frontend):**
    * 框架: SvelteKit
    * 样式: Tailwind CSS
    * 状态管理: Svelte Stores
* **后端 (Backend):**
    * 框架: Flask (Python)
    * API: RESTful API
    * 用户认证: JWT / OAuth (待定)
* **数据库 (Database):**
    * PostgreSQL
* **未来集成 (Future Integration):**
    * 大型语言模型 (LLM) API (如 OpenAI, Google Gemini) 用于智能分析与内容生成。

## 📝 设计理念与原则

* **用户中心 (User-Centric):** 始终以用户的需求和体验为核心。
* **专注与简化 (Focus & Simplification):** 界面设计力求清晰直观，避免信息过载，帮助用户聚焦核心任务。
* **模块化与解耦 (Modularity & Decoupling):** 各功能模块既独立又互相关联，易于维护和扩展。
* **平衡规划与行动 (Balancing Vision & Action):** 特别是在“打算做”模块，致力于在远期规划的激励性和可行动性之间找到平衡。
* **专业且激励人心 (Professional & Inspiring):** 视觉和交互设计旨在营造专业、可信赖且能激发用户积极性的氛围。

## 📈 项目状态

* \[请在此处填写当前项目状态，例如：MVP开发中 / Phase 1 功能已完成 / 内部测试阶段等\]
* 我们正积极地按照项目规划（详见 `项目开发基本方针.txt`）推进开发。

## 🚀 快速开始 (Getting Started)

*(此部分可由实际开发者根据项目部署情况填写)*

