#!/bin/bash
# 启动后端和前端服务

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

# 检查SQLite数据库
check_sqlite() {
    print_header "检查SQLite数据库"
    
    # 检查instance目录是否存在
    if [ ! -d "backend/instance" ]; then
        print_warning "未找到instance目录。正在创建..."
        mkdir -p backend/instance
    fi
    
    # 检查SQLite数据库文件是否存在
    if [ ! -f "backend/instance/dev.sqlite" ]; then
        print_warning "未找到SQLite数据库文件。正在初始化..."
        ./setup_sqlite.sh
    else
        print_success "SQLite数据库文件已存在。"
    fi
}

# 启动后端服务
start_backend() {
    print_header "启动后端服务"
    
    # 检查后端服务是否已经在运行
    if nc -z localhost 5000 2>/dev/null; then
        print_warning "后端服务已经在运行（端口5000）。"
        return
    fi
    
    # 启动后端服务
    print_info "正在启动后端服务..."
    cd backend
    python run.py &
    BACKEND_PID=$!
    cd ..
    
    # 等待后端服务启动
    print_info "等待后端服务启动..."
    for i in {1..10}; do
        if nc -z localhost 5000 2>/dev/null; then
            print_success "后端服务已启动（端口5000）。"
            return
        fi
        sleep 1
    done
    
    print_warning "后端服务可能未成功启动。请检查日志。"
}

# 启动前端服务
start_frontend() {
    print_header "启动前端服务"
    
    # 检查前端服务是否已经在运行
    if nc -z localhost 5173 2>/dev/null; then
        print_warning "前端服务已经在运行（端口5173）。"
        return
    fi
    
    # 检查npm是否安装
    if ! command -v npm &> /dev/null; then
        print_error "npm未安装。请安装Node.js和npm后重试。"
        return
    fi
    
    # 启动前端服务
    print_info "正在启动前端服务..."
    cd svelte@latest
    npm run dev &
    FRONTEND_PID=$!
    cd ..
    
    # 等待前端服务启动
    print_info "等待前端服务启动..."
    for i in {1..10}; do
        if nc -z localhost 5173 2>/dev/null; then
            print_success "前端服务已启动（端口5173）。"
            return
        fi
        sleep 1
    done
    
    print_warning "前端服务可能未成功启动。请检查日志。"
}

# 测试API连接
test_api() {
    print_header "测试API连接"
    
    # 等待服务完全启动
    print_info "等待服务完全启动..."
    sleep 3
    
    # 运行API连接测试
    print_info "正在测试API连接..."
    ./test_api_connection.py
}

# 主函数
main() {
    print_header "服务启动工具"
    
    # 检查SQLite数据库
    check_sqlite
    
    # 启动后端服务
    start_backend
    
    # 启动前端服务
    start_frontend
    
    # 测试API连接
    test_api
    
    print_header "服务已启动"
    print_success "后端服务正在运行（端口5000）。"
    print_success "前端服务正在运行（端口5173）。"
    print_info "您可以在浏览器中访问前端应用："
    echo -e "${CYAN}http://localhost:5173${NC}"
    
    # 保持脚本运行，直到用户按下Ctrl+C
    print_info "按Ctrl+C停止服务..."
    trap "kill $BACKEND_PID 2>/dev/null; kill $FRONTEND_PID 2>/dev/null; echo -e \"\n${GREEN}服务已停止。${NC}\"" EXIT
    wait
}

# 执行主函数
main
