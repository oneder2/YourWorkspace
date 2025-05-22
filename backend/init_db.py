#!/usr/bin/env python3
"""
SQLite数据库初始化脚本
此脚本用于初始化SQLite数据库，创建所有必要的表并添加示例数据。
"""

import os
import sys
import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 导入应用和模型
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.user_profile import UserProfile
from app.models.token_blocklist import TokenBlocklist
from app.models.todo_item import TodoItem
from app.models.achievement import Achievement
from app.models.future_plan import FuturePlan

def init_db():
    """初始化数据库"""
    print("初始化SQLite数据库...")

    # 确保instance目录存在
    instance_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
        print(f"创建了instance目录: {instance_dir}")

    # 设置数据库文件路径
    db_file = os.path.join(instance_dir, 'dev.sqlite')
    test_db_file = os.path.join(instance_dir, 'test.sqlite')
    prod_db_file = os.path.join(instance_dir, 'prod.sqlite')

    # 删除现有的数据库文件
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"删除了现有的数据库文件: {db_file}")

    # 创建空的数据库文件
    with open(db_file, 'w') as f:
        pass
    print(f"创建了空的数据库文件: {db_file}")

    # 复制开发数据库到测试和生产数据库
    with open(test_db_file, 'w') as f:
        pass
    print(f"创建了空的测试数据库文件: {test_db_file}")

    with open(prod_db_file, 'w') as f:
        pass
    print(f"创建了空的生产数据库文件: {prod_db_file}")

    # 确保文件权限正确
    os.chmod(db_file, 0o666)  # 设置读写权限
    os.chmod(test_db_file, 0o666)  # 设置读写权限
    os.chmod(prod_db_file, 0o666)  # 设置读写权限
    print(f"设置了数据库文件权限")

    # 创建Flask应用实例
    app = create_app('development')

    # 创建数据库表
    with app.app_context():
        # 创建所有表
        db.create_all()
        print("创建了数据库表")

        # 检查是否已存在测试用户
        test_user = User.query.filter_by(email="test@example.com").first()
        if not test_user:
            # 创建测试用户
            test_user = User(
                username="testuser",
                email="test@example.com",
                password="password123"
            )
            db.session.add(test_user)
            db.session.commit()
            print("创建了测试用户")

            # 创建示例数据
            create_sample_data(test_user.id)
        else:
            print(f"测试用户已存在 (ID: {test_user.id})")

            # 检查是否需要创建示例数据
            todo_count = TodoItem.query.filter_by(user_id=test_user.id).count()
            achievement_count = Achievement.query.filter_by(user_id=test_user.id).count()
            plan_count = FuturePlan.query.filter_by(user_id=test_user.id).count()

            if todo_count == 0 and achievement_count == 0 and plan_count == 0:
                print("未找到示例数据，正在创建...")
                create_sample_data(test_user.id)
            else:
                print(f"已存在示例数据 (待办事项: {todo_count}, 成就: {achievement_count}, 未来计划: {plan_count})")

        print("SQLite数据库初始化完成")

def create_sample_data(user_id):
    """为测试用户创建示例数据"""
    # 创建示例待办事项
    todos = [
        TodoItem(
            user_id=user_id,
            title="完成项目设置",
            description="设置开发环境并初始化项目。",
            status="completed",
            priority="high",
            is_current_focus=False
        ),
        TodoItem(
            user_id=user_id,
            title="实现用户认证",
            description="添加用户注册、登录和认证功能。",
            status="in_progress",
            priority="high",
            is_current_focus=True
        ),
        TodoItem(
            user_id=user_id,
            title="设计数据库架构",
            description="为应用程序创建数据库架构。",
            status="pending",
            priority="medium",
            is_current_focus=False
        )
    ]

    db.session.add_all(todos)
    db.session.commit()
    print(f"创建了 {len(todos)} 个示例待办事项")

    # 创建示例成就
    achievements = [
        Achievement(
            user_id=user_id,
            title="完成前端开发课程",
            description="完成了现代前端开发的综合课程。",
            date_achieved=datetime.date(2023, 1, 15),
            core_skills_json=["HTML", "CSS", "JavaScript", "React"]
        ),
        Achievement(
            user_id=user_id,
            title="发布第一个Web应用",
            description="成功将第一个Web应用部署到生产环境。",
            date_achieved=datetime.date(2023, 3, 20),
            core_skills_json=["Node.js", "Express", "MongoDB", "Deployment"]
        )
    ]

    db.session.add_all(achievements)
    db.session.commit()
    print(f"创建了 {len(achievements)} 个示例成就")

    # 创建示例未来计划
    plans = [
        FuturePlan(
            user_id=user_id,
            title="学习机器学习",
            description="完成机器学习基础课程。",
            goal_type="learning",
            target_date=datetime.date(2023, 12, 31),
            status="active"
        ),
        FuturePlan(
            user_id=user_id,
            title="构建移动应用",
            description="开发并发布一个移动应用。",
            goal_type="project",
            target_date=datetime.date(2024, 6, 30),
            status="active"
        )
    ]

    db.session.add_all(plans)
    db.session.commit()
    print(f"创建了 {len(plans)} 个示例未来计划")

if __name__ == "__main__":
    init_db()
