# YourWorkspace 后端服务

基于Flask的RESTful API后端服务，提供用户认证、任务管理、成就跟踪和计划管理功能。

## 技术栈

- **框架**: Flask 3.1.0
- **数据库**: SQLite (开发) / PostgreSQL (生产可选)
- **认证**: JWT + Flask-JWT-Extended
- **ORM**: SQLAlchemy + Flask-SQLAlchemy
- **依赖管理**: Poetry
- **WSGI服务器**: Gunicorn (生产环境)

## 快速开始

### 先决条件

- Python 3.12+
- Poetry (推荐) 或 pip

### 安装依赖

#### 使用Poetry (推荐)
```bash
# 安装Poetry (如果未安装)
curl -sSL https://install.python-poetry.org | python3 -

# 安装项目依赖
poetry install
```

#### 使用pip
```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 环境配置

1. 创建环境变量文件：
```bash
cp ../.env.example .env
```

2. 编辑`.env`文件，设置必要的环境变量：
```bash
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here
FLASK_CONFIG=development
```

### 数据库初始化

```bash
# 使用Poetry
poetry run python init_db.py

# 或使用pip
python init_db.py
```

### 启动开发服务器

```bash
# 使用Poetry
poetry run python run.py

# 或使用pip
python run.py
```

服务器将在 http://localhost:5000 启动

## API端点

### 认证相关
- `GET /api/v1/auth/ping` - 健康检查
- `POST /api/v1/auth/register` - 用户注册
- `POST /api/v1/auth/login` - 用户登录
- `POST /api/v1/auth/logout` - 用户登出
- `POST /api/v1/auth/refresh` - 刷新令牌

### 用户档案
- `GET /api/v1/anchor/profile` - 获取用户档案
- `PUT /api/v1/anchor/profile` - 更新用户档案

### 待办事项
- `GET /api/v1/todo/todos` - 获取待办事项列表
- `POST /api/v1/todo/todos` - 创建待办事项
- `PUT /api/v1/todo/todos/{id}` - 更新待办事项
- `DELETE /api/v1/todo/todos/{id}` - 删除待办事项

### 成就管理
- `GET /api/v1/achievements/` - 获取成就列表
- `POST /api/v1/achievements/` - 创建成就
- `PUT /api/v1/achievements/{id}` - 更新成就
- `DELETE /api/v1/achievements/{id}` - 删除成就

### 计划管理
- `GET /api/v1/plans/` - 获取计划列表
- `POST /api/v1/plans/` - 创建计划
- `PUT /api/v1/plans/{id}` - 更新计划
- `DELETE /api/v1/plans/{id}` - 删除计划

## 测试

### 运行单元测试
```bash
# 使用Poetry
poetry run pytest

# 或使用pip
pytest
```

### API测试
```bash
# 启动服务器后运行API测试
poetry run python test_api.py
```

## 生产部署

### 使用Gunicorn
```bash
# 安装Gunicorn (已包含在依赖中)
poetry run gunicorn --bind 0.0.0.0:5000 --workers 4 run:app
```

### 环境变量
生产环境需要设置以下环境变量：
```bash
FLASK_CONFIG=production
SECRET_KEY=your_production_secret_key
JWT_SECRET_KEY=your_production_jwt_secret_key
DATABASE_URL=your_database_url  # 可选，默认使用SQLite
```

## 项目结构

```
backend/
├── app/                    # 主应用包
│   ├── __init__.py        # 应用工厂
│   ├── config.py          # 配置类
│   ├── extensions.py      # Flask扩展
│   ├── api/               # API蓝图
│   │   ├── auth_bp.py     # 认证API
│   │   ├── anchor_bp.py   # 用户档案API
│   │   ├── todo_bp.py     # 待办事项API
│   │   ├── achievements_bp.py # 成就API
│   │   └── plans_bp.py    # 计划API
│   ├── models/            # 数据库模型
│   │   ├── user.py        # 用户模型
│   │   ├── todo_item.py   # 待办事项模型
│   │   ├── achievement.py # 成就模型
│   │   └── future_plan.py # 计划模型
│   └── utils/             # 工具函数
├── migrations/            # 数据库迁移
├── tests/                 # 测试文件
├── instance/              # 实例文件夹（数据库等）
├── run.py                 # 应用入口点
├── init_db.py            # 数据库初始化脚本
├── test_api.py           # API测试脚本
├── pyproject.toml        # Poetry配置
└── requirements.txt      # pip依赖列表
```

## 故障排除

### 常见问题

1. **数据库连接错误**
   - 确保已运行 `python init_db.py`
   - 检查 `instance/` 目录是否存在

2. **依赖安装失败**
   - 确保Python版本为3.12+
   - 尝试更新pip: `pip install --upgrade pip`

3. **端口占用**
   - 更改端口: `export PORT=5001`
   - 或杀死占用进程: `lsof -ti:5000 | xargs kill`

### 日志调试

开发模式下，详细日志会输出到控制台。生产环境建议配置日志文件：

```python
import logging
logging.basicConfig(level=logging.INFO)
```

## 贡献指南

1. 遵循PEP 8代码风格
2. 为新功能添加测试
3. 更新相关文档
4. 提交前运行测试套件

## 许可证

MIT License
