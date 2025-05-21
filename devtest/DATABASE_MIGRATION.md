# 数据库迁移指南

本文档提供了在PostgreSQL和SQLite之间迁移数据的指南，确保两种数据库具有相同的表结构和数据，使程序能在两种数据库上正常运行。

## 背景

项目最初使用PostgreSQL作为数据库，但为了简化开发和部署，我们添加了对SQLite的支持。这使得开发人员可以在不安装PostgreSQL的情况下进行开发，同时也使得部署更加简单。

## 工具说明

我们提供了两个工具来帮助您在PostgreSQL和SQLite之间迁移数据：

1. **db_migration_tool.py**：一个Python脚本，用于在PostgreSQL和SQLite之间导出、导入和迁移数据。
2. **setup_sqlite.sh**：一个Shell脚本，用于自动设置SQLite数据库并从PostgreSQL迁移数据（如果可用）。

## 快速开始

如果您想快速设置SQLite数据库并从PostgreSQL迁移数据，只需运行以下命令：

```bash
chmod +x setup_sqlite.sh
./setup_sqlite.sh
```

这将：
1. 检查必要的Python包是否已安装
2. 更新`.env`文件以使用SQLite
3. 检查PostgreSQL连接（如果可用）
4. 从PostgreSQL迁移数据到SQLite（如果PostgreSQL可用）
5. 如果PostgreSQL不可用，则初始化SQLite数据库并创建示例数据

## 手动使用迁移工具

如果您想手动控制迁移过程，可以直接使用`db_migration_tool.py`脚本。

### 安装依赖

首先，确保您已安装所有必要的Python包：

```bash
pip install flask flask-sqlalchemy flask-migrate flask-bcrypt flask-jwt-extended python-dotenv sqlalchemy
```

### 检查数据库连接

检查PostgreSQL和SQLite连接：

```bash
python db_migration_tool.py --action check --source postgres
python db_migration_tool.py --action check --source sqlite
```

### 初始化数据库

初始化PostgreSQL和SQLite数据库：

```bash
python db_migration_tool.py --action init --source postgres --target sqlite
```

这将在两个数据库中创建所有必要的表，并添加示例数据。

### 从PostgreSQL导出数据

将PostgreSQL中的数据导出到JSON文件：

```bash
python db_migration_tool.py --action export --source postgres --file postgres_data.json
```

### 将数据导入SQLite

将JSON文件中的数据导入SQLite：

```bash
python db_migration_tool.py --action import --target sqlite --file postgres_data.json
```

### 直接迁移数据

直接将数据从PostgreSQL迁移到SQLite：

```bash
python db_migration_tool.py --action migrate --source postgres --target sqlite
```

## 数据库配置

### PostgreSQL配置

PostgreSQL配置在`backend/.env`文件中：

```
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_DB_DEV=mydatabase
POSTGRES_DB_TEST=testdatabase
POSTGRES_DB_PROD=your_prod_db
```

### SQLite配置

SQLite配置也在`backend/.env`文件中：

```
DEV_DATABASE_URL="sqlite:///instance/dev.sqlite"
TEST_DATABASE_URL="sqlite:///instance/test.sqlite"
```

## 切换数据库

要在PostgreSQL和SQLite之间切换，只需更新`backend/.env`文件中的`DEV_DATABASE_URL`和`TEST_DATABASE_URL`：

### 使用PostgreSQL

```
DEV_DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB_DEV}"
TEST_DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB_TEST}"
```

### 使用SQLite

```
DEV_DATABASE_URL="sqlite:///instance/dev.sqlite"
TEST_DATABASE_URL="sqlite:///instance/test.sqlite"
```

## 注意事项

1. **数据类型兼容性**：PostgreSQL和SQLite之间存在一些数据类型差异，但我们的模型设计已考虑到这一点，确保两种数据库都能正常工作。

2. **JSON支持**：SQLite对JSON的支持不如PostgreSQL，但我们的代码已经处理了这种差异。

3. **性能**：SQLite适用于开发和小型应用，但对于生产环境和高并发场景，PostgreSQL通常是更好的选择。

4. **备份**：在进行数据迁移之前，建议备份您的数据。

5. **数据库文件位置**：SQLite数据库文件位于`backend/instance/`目录中。

## 故障排除

### 连接问题

- **PostgreSQL连接失败**：检查PostgreSQL服务是否正在运行，以及`.env`文件中的连接信息是否正确。

- **SQLite连接失败**：检查`instance`目录是否存在并且可写。

### 迁移问题

- **数据导出失败**：检查PostgreSQL连接和权限。

- **数据导入失败**：检查JSON文件格式是否正确，以及SQLite数据库是否可写。

### 其他问题

如果您遇到其他问题，请检查日志输出以获取更多信息。
