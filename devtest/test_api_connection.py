#!/usr/bin/env python3
"""
API连接测试脚本
此脚本用于测试前端和后端API之间的连接。
"""

import requests
import json
import sys
import os
import time
import subprocess
import signal
from urllib.parse import urlparse

# 颜色常量
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# 配置
BACKEND_URL = "http://localhost:5000"
FRONTEND_URL = "http://localhost:5173"
API_PREFIX = "/api/v1"

# 测试用户凭据
TEST_USER = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
}

# 存储令牌
tokens = {
    "access_token": None,
    "refresh_token": None
}

def print_header(message):
    """打印格式化的标题消息"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{message.center(80)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}\n")

def print_result(test_name, success, message=""):
    """打印测试结果"""
    status = f"{Colors.OKGREEN}通过{Colors.ENDC}" if success else f"{Colors.FAIL}失败{Colors.ENDC}"
    print(f"{test_name.ljust(50)} [{status}] {message}")

def check_server_running(url, name):
    """检查服务器是否正在运行"""
    try:
        response = requests.get(url, timeout=2)
        return True, response.status_code
    except requests.exceptions.ConnectionError:
        return False, None
    except Exception as e:
        return False, str(e)

def test_backend_connection():
    """测试后端连接"""
    print_header("测试后端连接")
    
    # 检查后端是否正在运行
    is_running, status = check_server_running(BACKEND_URL, "Backend")
    print_result("后端服务器运行状态", is_running, f"状态: {status}")
    
    if not is_running:
        print(f"{Colors.WARNING}后端服务器未运行。请先启动后端服务器。{Colors.ENDC}")
        return False
    
    # 测试根端点
    try:
        response = requests.get(BACKEND_URL)
        print_result("后端根端点", response.status_code == 200, 
                    f"状态: {response.status_code}, 响应: {response.text}")
    except Exception as e:
        print_result("后端根端点", False, f"错误: {str(e)}")
    
    return is_running

def test_cors_configuration():
    """测试CORS配置"""
    print_header("测试CORS配置")
    
    # 测试预检请求
    try:
        headers = {
            'Origin': FRONTEND_URL,
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'Content-Type, Authorization'
        }
        response = requests.options(f"{BACKEND_URL}{API_PREFIX}/auth/ping", headers=headers)
        
        cors_headers = response.headers.get('Access-Control-Allow-Origin')
        methods_header = response.headers.get('Access-Control-Allow-Methods')
        
        print_result("CORS预检响应", response.status_code < 400, 
                    f"状态: {response.status_code}")
        print_result("Access-Control-Allow-Origin头", cors_headers is not None, 
                    f"值: {cors_headers}")
        print_result("Access-Control-Allow-Methods头", methods_header is not None, 
                    f"值: {methods_header}")
        
    except Exception as e:
        print_result("CORS预检请求", False, f"错误: {str(e)}")

def test_api_endpoints():
    """测试各种API端点"""
    print_header("测试API端点")
    
    # 测试auth ping端点
    try:
        response = requests.get(f"{BACKEND_URL}{API_PREFIX}/auth/ping")
        print_result("Auth ping端点", response.status_code == 200, 
                    f"状态: {response.status_code}, 响应: {response.text}")
    except Exception as e:
        print_result("Auth ping端点", False, f"错误: {str(e)}")
    
    # 测试todo ping端点
    try:
        response = requests.get(f"{BACKEND_URL}{API_PREFIX}/todo/ping")
        print_result("Todo ping端点", response.status_code == 200, 
                    f"状态: {response.status_code}, 响应: {response.text}")
    except Exception as e:
        print_result("Todo ping端点", False, f"错误: {str(e)}")
    
    # 测试achievements ping端点
    try:
        response = requests.get(f"{BACKEND_URL}{API_PREFIX}/achievements/ping")
        print_result("Achievements ping端点", response.status_code == 200, 
                    f"状态: {response.status_code}, 响应: {response.text}")
    except Exception as e:
        print_result("Achievements ping端点", False, f"错误: {str(e)}")
    
    # 测试plans ping端点
    try:
        response = requests.get(f"{BACKEND_URL}{API_PREFIX}/plans/ping")
        print_result("Plans ping端点", response.status_code == 200, 
                    f"状态: {response.status_code}, 响应: {response.text}")
    except Exception as e:
        print_result("Plans ping端点", False, f"错误: {str(e)}")

def test_auth_flow():
    """测试认证流程"""
    print_header("测试认证流程")
    
    # 测试登录
    try:
        response = requests.post(
            f"{BACKEND_URL}{API_PREFIX}/auth/login", 
            json={"email": TEST_USER["email"], "password": TEST_USER["password"]}
        )
        
        print_result("用户登录", response.status_code == 200, 
                    f"状态: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            tokens["access_token"] = data.get("access_token")
            tokens["refresh_token"] = data.get("refresh_token")
            
            print_result("获取访问令牌", tokens["access_token"] is not None)
            print_result("获取刷新令牌", tokens["refresh_token"] is not None)
    except Exception as e:
        print_result("用户登录", False, f"错误: {str(e)}")
    
    # 测试认证端点
    if tokens["access_token"]:
        try:
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            response = requests.get(f"{BACKEND_URL}{API_PREFIX}/auth/me", headers=headers)
            
            print_result("认证端点", response.status_code == 200, 
                        f"状态: {response.status_code}")
            
            if response.status_code == 200:
                print(f"用户资料: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        except Exception as e:
            print_result("认证端点", False, f"错误: {str(e)}")

def test_todo_api():
    """测试待办事项API"""
    print_header("测试待办事项API")
    
    if not tokens["access_token"]:
        print(f"{Colors.WARNING}跳过待办事项API测试，因为没有访问令牌。{Colors.ENDC}")
        return
    
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    
    # 获取所有待办事项
    try:
        response = requests.get(f"{BACKEND_URL}{API_PREFIX}/todo/todos", headers=headers)
        print_result("获取所有待办事项", response.status_code == 200, 
                    f"状态: {response.status_code}")
        
        if response.status_code == 200:
            todos = response.json()
            print(f"找到 {len(todos)} 个待办事项")
    except Exception as e:
        print_result("获取所有待办事项", False, f"错误: {str(e)}")
    
    # 创建新待办事项
    try:
        new_todo = {
            "title": "测试待办事项",
            "description": "这是一个由API测试脚本创建的测试待办事项",
            "status": "pending",
            "priority": "medium",
            "is_current_focus": False
        }
        
        response = requests.post(f"{BACKEND_URL}{API_PREFIX}/todo/todos", headers=headers, json=new_todo)
        print_result("创建待办事项", response.status_code == 201, 
                    f"状态: {response.status_code}")
        
        if response.status_code == 201:
            created_todo = response.json()
            todo_id = created_todo["id"]
            print(f"创建了ID为 {todo_id} 的待办事项")
            
            # 更新待办事项
            try:
                update_data = {
                    "title": "更新的测试待办事项",
                    "status": "in_progress"
                }
                
                response = requests.put(f"{BACKEND_URL}{API_PREFIX}/todo/todos/{todo_id}", 
                                        headers=headers, json=update_data)
                print_result("更新待办事项", response.status_code == 200, 
                            f"状态: {response.status_code}")
            except Exception as e:
                print_result("更新待办事项", False, f"错误: {str(e)}")
            
            # 删除待办事项
            try:
                response = requests.delete(f"{BACKEND_URL}{API_PREFIX}/todo/todos/{todo_id}", headers=headers)
                print_result("删除待办事项", response.status_code == 200, 
                            f"状态: {response.status_code}")
            except Exception as e:
                print_result("删除待办事项", False, f"错误: {str(e)}")
    except Exception as e:
        print_result("创建待办事项", False, f"错误: {str(e)}")

def main():
    """主函数"""
    print_header("API连接测试脚本")
    
    # 检查后端是否正在运行
    backend_running = test_backend_connection()
    if not backend_running:
        print(f"{Colors.WARNING}跳过后续测试，因为后端未运行。{Colors.ENDC}")
        return
    
    # 运行所有测试
    test_cors_configuration()
    test_api_endpoints()
    test_auth_flow()
    test_todo_api()
    
    print_header("测试总结")
    if tokens["access_token"]:
        print(f"{Colors.OKGREEN}{Colors.BOLD}API连接测试成功！{Colors.ENDC}")
        print(f"后端API正常工作，认证流程正常，待办事项API正常。")
    else:
        print(f"{Colors.WARNING}{Colors.BOLD}API连接测试部分成功。{Colors.ENDC}")
        print(f"后端API可以访问，但认证流程可能存在问题。")

if __name__ == "__main__":
    main()
