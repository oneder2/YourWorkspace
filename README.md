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

## 部署

### 使用Docker Compose（推荐）

1. 克隆仓库:
   ```bash
   git clone <repository-url>
   cd YourWorkplace
   ```

2. 在根目录创建`.env`文件，包含以下变量:
   ```
   SECRET_KEY=your_secret_key
   JWT_SECRET_KEY=your_jwt_secret_key
   ```

3. 使用部署脚本启动应用:
   ```bash
   chmod +x deploy.sh
   ./deploy.sh start
   ```

4. 访问应用: http://localhost

### 手动部署

#### 后端

1. 导航到后端目录:
   ```bash
   cd backend
   ```

2. 使用Poetry安装依赖:
   ```bash
   poetry install
   ```

3. 初始化数据库:
   ```bash
   python init_db.py
   ```

4. 启动后端服务器:
   ```bash
   poetry run python run.py
   ```

#### 前端

1. 导航到前端目录:
   ```bash
   cd svelte@latest
   ```

2. 安装依赖:
   ```bash
   npm install
   ```

3. 启动开发服务器:
   ```bash
   npm run dev
   ```

## 开发

### 后端

后端是一个Flask应用，具有以下结构:

- `app/`: 主应用包
  - `api/`: API端点
  - `models/`: 数据库模型
  - `utils/`: 实用函数
- `migrations/`: 数据库迁移
- `tests/`: 测试用例

### 前端

前端是一个Svelte应用，具有以下结构:

- `src/`: 源代码
  - `lib/`: 库代码
    - `components/`: 可重用组件
    - `services/`: API服务
    - `store/`: Svelte存储
  - `routes/`: 页面路由

## 测试

### 后端

运行后端测试:

```bash
cd backend
poetry run pytest
```

### 前端

运行前端测试:

```bash
cd svelte@latest
npm run test
```

## 原始功能设想

#### 主要功能：
1. 主界面展示个人技术、能力和项目经验

2. Todo-List界面存放目前的任务
    - 任务分级，大任务下会细分为若干小目标
    - 自行评定大任务是否完成
    - 完成时自己撰写完成情况
    - 由AI生成任务完成报告
    - 合并到主界面的个人信息

#### 额外功能：
1. 博客系统，类似日志
    - 在私有空间分享开发记录
    - 可以加装外链，同步共享到主流社交平台
2. 根据任务完成时间、创建时间等参数，生成月报和年报