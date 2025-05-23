# YourWorkplace 开发须知

## ⚠️ 重要声明

**本项目为AI生产力主导的项目，人工干预需要谨慎**

本项目主要由AI助手设计和开发，代码架构、业务逻辑和技术选型都经过AI的深度思考和优化。在进行人工修改时，请务必：

1. **理解现有架构** - 在修改前充分理解当前的代码结构和设计理念
2. **保持一致性** - 遵循已建立的编码规范和架构模式
3. **谨慎重构** - 避免大规模重构，优先考虑渐进式改进
4. **测试验证** - 任何修改都必须经过充分测试
5. **文档更新** - 修改后及时更新相关文档

## 项目架构理念

### AI驱动的设计原则

1. **模块化设计** - 每个功能模块独立，便于AI理解和维护
2. **类型安全** - 使用TypeScript确保代码的可预测性
3. **统一接口** - API设计遵循RESTful规范，便于AI生成和理解
4. **配置驱动** - 通过配置文件管理环境和功能开关
5. **自动化优先** - 优先使用自动化工具处理重复性任务

### 技术栈选择理由

- **后端Flask**: 简洁明了，AI易于理解和生成代码
- **前端Svelte**: 现代化框架，组件化思维符合AI开发模式
- **SQLite**: 轻量级数据库，便于开发和部署
- **Docker**: 容器化部署，环境一致性
- **Poetry**: Python依赖管理，版本控制精确

## 开发环境设置

### 先决条件

- Python 3.12+
- Node.js 20+
- Poetry
- Docker & Docker Compose (可选)
- Git

### 完整环境设置

```bash
# 1. 克隆项目
git clone <repository-url>
cd YourWorkplace

# 2. 设置后端环境
cd backend
poetry install
poetry run python init_db.py

# 3. 设置前端环境
cd ../svelte@latest
npm install

# 4. 配置环境变量
cp ../.env.example ../.env
# 编辑.env文件设置密钥

# 5. 启动开发服务器
# 终端1: 后端
cd backend && poetry run python run.py

# 终端2: 前端
cd svelte@latest && npm run dev
```

## 代码规范

### Python (后端)

```python
# 遵循PEP 8规范
# 使用类型注解
def create_user(username: str, email: str) -> User:
    """创建新用户"""
    return User(username=username, email=email)

# 使用docstring
class UserService:
    """用户服务类"""
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        return User.query.get(user_id)
```

### TypeScript (前端)

```typescript
// 使用严格类型
interface User {
  id: number;
  username: string;
  email: string;
}

// 使用async/await
async function fetchUser(id: number): Promise<User> {
  const response = await api.get(`/users/${id}`);
  return response.data;
}

// 组件类型定义
interface Props {
  user: User;
  onUpdate: (user: User) => void;
}
```

### Svelte组件

```svelte
<script lang="ts">
  // 类型定义在顶部
  interface Props {
    title: string;
    items: Item[];
  }
  
  let { title, items }: Props = $props();
  
  // 响应式声明
  $: filteredItems = items.filter(item => item.active);
</script>

<!-- 模板部分 -->
<div class="container">
  <h1>{title}</h1>
  {#each filteredItems as item}
    <div>{item.name}</div>
  {/each}
</div>

<style>
  /* 使用Tailwind CSS，避免自定义样式 */
</style>
```

## 数据库设计

### 核心表结构

```sql
-- 用户表
users (id, username, email, password_hash, created_at, updated_at)

-- 用户档案表
user_profiles (id, professional_title, one_liner_bio, skill, summary)

-- 待办事项表
todo_items (id, user_id, title, description, status, priority, is_current_focus)

-- 成就表
achievements (id, user_id, title, description, quantifiable_results, core_skills_json)

-- 未来计划表
future_plans (id, user_id, goal_type, title, description, target_date, status)
```

### 数据库迁移

```bash
# 创建迁移
cd backend
poetry run flask db migrate -m "描述"

# 应用迁移
poetry run flask db upgrade
```

## API设计规范

### RESTful接口

```
GET    /api/v1/resource      # 获取资源列表
POST   /api/v1/resource      # 创建资源
GET    /api/v1/resource/{id} # 获取单个资源
PUT    /api/v1/resource/{id} # 更新资源
DELETE /api/v1/resource/{id} # 删除资源
```

### 响应格式

```json
// 成功响应
{
  "success": true,
  "data": {...},
  "message": "操作成功"
}

// 错误响应
{
  "success": false,
  "error": "错误信息",
  "code": "ERROR_CODE"
}
```

## 测试策略

### 后端测试

```bash
# 运行所有测试
cd backend
poetry run pytest

# 运行特定测试
poetry run pytest tests/test_auth.py

# 测试覆盖率
poetry run pytest --cov=app
```

### 前端测试

```bash
# 类型检查
cd svelte@latest
npm run check

# 构建测试
npm run build
```

### API测试

```bash
# 启动后端服务后运行
cd backend
poetry run python test_api.py
```

## 部署指南

### 开发部署

```bash
# 后端
cd backend && poetry run python run.py

# 前端
cd svelte@latest && npm run dev
```

### 生产部署

```bash
# Docker方式
./deploy.sh start

# 手动方式
cd backend && poetry run gunicorn --bind 0.0.0.0:5000 run:app
cd svelte@latest && npm run build && npm run preview
```

## 常见开发任务

### 添加新的API端点

1. 在`backend/app/models/`中定义数据模型
2. 在`backend/app/api/`中创建蓝图
3. 在`backend/app/__init__.py`中注册蓝图
4. 更新前端API服务
5. 添加相应的测试

### 添加新页面

1. 在`svelte@latest/src/routes/`中创建页面
2. 更新导航组件
3. 添加必要的API调用
4. 测试响应式设计

### 修改数据库结构

1. 修改模型定义
2. 创建数据库迁移
3. 更新API接口
4. 更新前端类型定义
5. 运行测试确保兼容性

## 故障排除

### 常见问题

1. **数据库连接失败**
   ```bash
   # 重新初始化数据库
   cd backend && poetry run python init_db.py
   ```

2. **前端构建失败**
   ```bash
   # 清除缓存重新安装
   cd svelte@latest
   rm -rf node_modules .svelte-kit
   npm install
   ```

3. **API调用失败**
   - 检查后端服务是否启动
   - 验证API端点URL
   - 检查认证令牌

### 调试技巧

```python
# 后端调试
import logging
logging.basicConfig(level=logging.DEBUG)

# 在代码中添加断点
import pdb; pdb.set_trace()
```

```typescript
// 前端调试
console.log('Debug info:', data);

// 使用浏览器开发者工具
debugger;
```

## 性能优化

### 后端优化

- 使用数据库索引
- 实现查询缓存
- 优化SQL查询
- 使用连接池

### 前端优化

- 代码分割
- 懒加载组件
- 图片优化
- 缓存策略

## 安全考虑

- JWT令牌管理
- 输入验证和清理
- CORS配置
- 密码哈希
- SQL注入防护

## 贡献指南

1. **Fork项目**并创建功能分支
2. **遵循代码规范**和架构模式
3. **添加测试**覆盖新功能
4. **更新文档**说明变更
5. **提交PR**并详细描述修改内容

## 联系方式

如有技术问题或建议，请通过以下方式联系：

- 创建GitHub Issue
- 发送邮件至项目维护者
- 参与项目讨论

---

**记住：这是一个AI主导的项目，请在修改时保持对现有架构的尊重和理解。**
