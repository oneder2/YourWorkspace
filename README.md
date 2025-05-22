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