# space 前端应用

基于Svelte 5和SvelteKit构建的现代化单页应用，提供直观的用户界面用于任务管理、成就跟踪和计划制定。

## 技术栈

- **框架**: Svelte 5 + SvelteKit 2.16.0
- **样式**: Tailwind CSS 3.4.17
- **构建工具**: Vite 6.2.6
- **包管理**: npm
- **Web服务器**: Nginx (生产环境)

## 功能特性

- 🎯 **响应式设计** - 适配桌面和移动设备
- 🌙 **深色模式** - 支持明暗主题切换
- 🖼️ **自定义背景** - 支持上传个人背景图片
- ⚡ **快速加载** - 优化的构建和缓存策略
- 🔐 **安全认证** - JWT令牌管理
- 📱 **PWA就绪** - 支持离线使用

## 快速开始

### 先决条件

- Node.js 18+ (推荐使用 Node.js 20+)
- npm 或 yarn

### 安装依赖

```bash
# 使用npm
npm install

# 或使用yarn
yarn install
```

### 环境配置

1. 创建环境变量文件：
```bash
cp .env.example .env
```

2. 编辑`.env`文件：
```bash
# API基础URL - 开发环境使用 (空值表示直接调用API)
VITE_API_BASE_URL=

# 公共URL - 生产环境使用
PUBLIC_URL=http://localhost
```

### 启动开发服务器

```bash
# 启动开发服务器
npm run dev

# 或使用yarn
yarn dev
```

应用将在 http://localhost:5173 启动

### 构建生产版本

```bash
# 构建生产版本
npm run build

# 预览生产构建
npm run preview
```

## 页面结构

### 主要页面

1. **登录/注册页面** (`/login`, `/register`)
   - 用户认证界面
   - 表单验证和错误处理

2. **Done页面** (`/done`)
   - 成就展示和管理
   - 添加、编辑、删除成就

3. **Doing页面** (`/doing`)
   - 当前任务管理
   - 主要焦点设置
   - 任务状态跟踪

4. **Plan页面** (`/plan`)
   - 未来计划制定
   - 目标设置和跟踪

5. **Anchor页面** (`/anchor`)
   - 个人档案管理
   - 技能和经验展示

### 组件架构

```
src/
├── lib/
│   ├── components/
│   │   ├── common/          # 通用组件
│   │   │   ├── Modal.svelte
│   │   │   ├── Button.svelte
│   │   │   └── LoadingSpinner.svelte
│   │   ├── layout/          # 布局组件
│   │   │   ├── Navbar.svelte
│   │   │   ├── ArrowNav.svelte
│   │   │   └── Sidebar.svelte
│   │   ├── forms/           # 表单组件
│   │   └── ui/              # UI组件
│   ├── services/            # API服务
│   │   ├── api.ts
│   │   ├── authService.ts
│   │   └── apiClient.ts
│   ├── store/               # 状态管理
│   │   ├── authStore.ts
│   │   └── themeStore.ts
│   └── utils/               # 工具函数
├── routes/                  # 页面路由
│   ├── (app)/              # 认证后的页面
│   ├── login/
│   └── register/
└── app.html                # HTML模板
```

## 开发指南

### 代码风格

- 使用TypeScript进行类型安全
- 遵循Svelte官方风格指南
- 使用Prettier进行代码格式化
- 使用ESLint进行代码检查

### 状态管理

使用Svelte的内置store进行状态管理：

```typescript
// 认证状态
import { authStore } from '$lib/store/authStore';

// 主题状态
import { themeStore } from '$lib/store/themeStore';
```

### API调用

使用统一的API客户端：

```typescript
import { api } from '$lib/services/api';

// GET请求
const data = await api.get('/endpoint');

// POST请求
const result = await api.post('/endpoint', { data });
```

### 样式系统

使用Tailwind CSS进行样式设计：

```svelte
<div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md">
  <h2 class="text-xl font-semibold text-gray-900 dark:text-white">
    标题
  </h2>
</div>
```

## 构建和部署

### 开发构建

```bash
# 启动开发服务器（热重载）
npm run dev

# 类型检查
npm run check

# 监听模式类型检查
npm run check:watch
```

### 生产构建

```bash
# 构建生产版本
npm run build

# 预览生产构建
npm run preview
```

## 故障排除

### 常见问题

1. **构建失败**
   ```bash
   # 清除缓存
   rm -rf node_modules .svelte-kit
   npm install
   ```

2. **API连接问题**
   - 检查后端服务是否启动
   - 验证API基础URL配置
   - 检查CORS设置

3. **样式问题**
   - 确保Tailwind CSS正确配置
   - 检查PostCSS配置
   - 验证CSS导入路径

### 浏览器支持

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 许可证

MIT License
