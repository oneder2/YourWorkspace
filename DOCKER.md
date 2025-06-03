# Docker 部署指南

本文档提供了使用Docker部署YourWorkspace应用的详细说明。

## 先决条件

- Docker 20.10.0或更高版本
- Docker Compose 2.0.0或更高版本
- Git

## 快速开始

1. 克隆仓库:
   ```bash
   git clone <repository-url>
   cd YourWorkspace
   ```

2. 使用部署脚本启动应用:
   ```bash
   chmod +x deploy.sh
   ./deploy.sh start
   ```

3. 访问应用: http://localhost

## 配置

### 环境变量

在根目录创建`.env`文件，包含以下变量:

```
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
```

这些密钥用于加密会话和JWT令牌。在生产环境中，请使用强密钥。

### 数据持久化

应用数据存储在SQLite数据库中，该数据库位于`backend/instance`目录。此目录已配置为Docker卷，以确保数据在容器重启后仍然存在。

## Docker Compose配置

`docker-compose.yml`文件定义了两个服务:

1. **backend**: Flask后端API
   - 构建自`backend/Dockerfile`
   - 暴露端口5000
   - 使用卷持久化数据库

2. **frontend**: Svelte前端应用
   - 构建自`svelte@latest/Dockerfile`
   - 暴露端口80
   - 依赖于backend服务

## 部署脚本

`deploy.sh`脚本提供了以下命令:

- `./deploy.sh start`: 构建并启动容器
- `./deploy.sh stop`: 停止容器
- `./deploy.sh restart`: 重启容器
- `./deploy.sh logs`: 显示容器日志

## 生产环境部署

对于生产环境部署，请考虑以下事项:

1. **安全性**:
   - 使用强密钥
   - 配置HTTPS
   - 限制访问权限

2. **性能**:
   - 调整Gunicorn工作进程数
   - 配置Nginx缓存

3. **监控**:
   - 设置容器健康检查
   - 配置日志聚合

## 故障排除

### 常见问题

1. **无法连接到应用**:
   - 检查容器是否正在运行: `docker-compose ps`
   - 检查容器日志: `./deploy.sh logs`

2. **数据库错误**:
   - 检查`backend/instance`目录是否存在
   - 检查数据库文件权限

3. **前端无法连接到后端**:
   - 检查Nginx配置
   - 检查后端健康检查

### 日志

查看容器日志:

```bash
./deploy.sh logs
```

或者单独查看每个服务的日志:

```bash
docker-compose logs backend
docker-compose logs frontend
```

## 自定义

### 自定义端口

要更改应用端口，请编辑`docker-compose.yml`文件:

```yaml
services:
  frontend:
    ports:
      - "8080:80"  # 将端口从80更改为8080
```

### 自定义数据库位置

要更改数据库位置，请编辑`docker-compose.yml`文件:

```yaml
services:
  backend:
    volumes:
      - ./data:/app/instance  # 将数据库存储在./data目录
```
