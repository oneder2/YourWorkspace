#!/bin/bash
# 设置SQLite数据库并从PostgreSQL迁移数据

# 颜色常量
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # 无颜色

# 打印标题
print_header() {
    echo -e "\n${PURPLE}=========================================================================${NC}"
    echo -e "${PURPLE}${1}${NC}"
    echo -e "${PURPLE}=========================================================================${NC}\n"
}

# 打印信息
print_info() {
    echo -e "${BLUE}[INFO]${NC} ${1}"
}

# 打印成功
print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} ${1}"
}

# 打印警告
print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} ${1}"
}

# 打印错误
print_error() {
    echo -e "${RED}[ERROR]${NC} ${1}"
}

# 检查Python是否安装
check_python() {
    if ! command -v python &> /dev/null; then
        print_error "Python未安装。请安装Python 3.x后重试。"
        exit 1
    fi
    
    # 检查Python版本
    python_version=$(python --version 2>&1 | awk '{print $2}')
    print_info "Python版本: ${python_version}"
    
    # 检查必要的Python包
    print_info "检查必要的Python包..."
    python -c "import flask, sqlalchemy, dotenv" 2>/dev/null
    if [ $? -ne 0 ]; then
        print_warning "缺少必要的Python包。正在安装..."
        pip install flask flask-sqlalchemy flask-migrate flask-bcrypt flask-jwt-extended python-dotenv sqlalchemy
    else
        print_success "所有必要的Python包已安装。"
    fi
}

# 检查数据库连接
check_db_connection() {
    print_header "检查数据库连接"
    
    # 检查PostgreSQL连接
    python db_migration_tool.py --action check --source postgres
    pg_status=$?
    
    # 检查SQLite连接
    python db_migration_tool.py --action check --source sqlite
    sqlite_status=$?
    
    if [ $pg_status -ne 0 ] && [ $sqlite_status -ne 0 ]; then
        print_error "PostgreSQL和SQLite连接均失败。请检查配置。"
        exit 1
    fi
    
    if [ $pg_status -ne 0 ]; then
        print_warning "PostgreSQL连接失败。将只初始化SQLite数据库。"
        return 1
    fi
    
    if [ $sqlite_status -ne 0 ]; then
        print_warning "SQLite连接失败。请检查配置。"
        return 2
    fi
    
    print_success "数据库连接检查完成。"
    return 0
}

# 初始化数据库
init_db() {
    print_header "初始化数据库"
    
    # 检查数据库连接
    check_db_connection
    connection_status=$?
    
    if [ $connection_status -eq 0 ]; then
        # PostgreSQL和SQLite连接均成功，执行迁移
        print_info "正在从PostgreSQL迁移数据到SQLite..."
        python db_migration_tool.py --action migrate --source postgres --target sqlite
    elif [ $connection_status -eq 1 ]; then
        # 只有SQLite连接成功，初始化SQLite
        print_info "正在初始化SQLite数据库..."
        python db_migration_tool.py --action init --source sqlite
    else
        # SQLite连接失败
        print_error "无法初始化SQLite数据库。请检查配置。"
        exit 1
    fi
    
    print_success "数据库初始化完成。"
}

# 更新.env文件
update_env_file() {
    print_header "更新.env文件"
    
    # 检查.env文件是否存在
    if [ ! -f backend/.env ]; then
        print_error "未找到.env文件。请确保backend/.env文件存在。"
        exit 1
    fi
    
    # 备份.env文件
    cp backend/.env backend/.env.bak
    print_info "已备份.env文件到backend/.env.bak"
    
    # 更新.env文件中的数据库配置
    sed -i 's/^DEV_DATABASE_URL=.*/DEV_DATABASE_URL="sqlite:\/\/\/instance\/dev.sqlite"/' backend/.env
    sed -i 's/^TEST_DATABASE_URL=.*/TEST_DATABASE_URL="sqlite:\/\/\/instance\/test.sqlite"/' backend/.env
    
    # 注释掉PostgreSQL配置
    sed -i 's/^DATABASE_URL=.*/# DATABASE_URL="postgresql:\/\/${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}\/${POSTGRES_DB_PROD}" # For Production/' backend/.env
    
    print_success ".env文件已更新，现在使用SQLite作为数据库。"
}

# 主函数
main() {
    print_header "SQLite数据库设置工具"
    
    # 检查Python
    check_python
    
    # 更新.env文件
    update_env_file
    
    # 初始化数据库
    init_db
    
    print_header "设置完成"
    print_success "SQLite数据库已设置完成，并已从PostgreSQL迁移数据（如果可用）。"
    print_info "您现在可以使用以下命令启动后端服务："
    echo -e "${CYAN}cd backend && python run.py${NC}"
}

# 执行主函数
main
