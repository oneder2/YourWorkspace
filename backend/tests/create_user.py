#!/usr/bin/env python3
"""
创建测试用户
此脚本用于创建测试用户。
"""

from app import create_app
from app.extensions import db
from app.models.user import User

def create_test_user():
    """创建测试用户"""
    print("创建测试用户...")
    
    # 创建Flask应用实例
    app = create_app('development')
    
    with app.app_context():
        # 检查是否已存在测试用户
        test_user = User.query.filter_by(email="test1@example.com").first()
        if not test_user:
            # 创建测试用户
            test_user = User(
                username="testuser1",
                email="test1@example.com",
                password="password123"
            )
            db.session.add(test_user)
            db.session.commit()
            print(f"创建了测试用户 (ID: {test_user.id})")
        else:
            print(f"测试用户已存在 (ID: {test_user.id})")
        
        print("测试用户创建完成")

if __name__ == "__main__":
    create_test_user()
