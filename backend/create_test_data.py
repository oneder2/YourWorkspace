#!/usr/bin/env python3
"""
创建测试数据
此脚本用于创建测试用户和示例数据。
"""

import datetime
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.todo_item import TodoItem
from app.models.achievement import Achievement
from app.models.future_plan import FuturePlan

def create_test_data():
    """创建测试数据"""
    print("创建测试数据...")

    # 创建Flask应用实例
    app = create_app('development')

    with app.app_context():
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
        else:
            print(f"测试用户已存在 (ID: {test_user.id})")

        # 创建示例数据
        create_sample_data(test_user.id)

        print("测试数据创建完成")

def create_sample_data(user_id):
    """为测试用户创建示例数据"""
    # 检查是否已存在示例数据
    todo_count = TodoItem.query.filter_by(user_id=user_id).count()
    achievement_count = Achievement.query.filter_by(user_id=user_id).count()
    plan_count = FuturePlan.query.filter_by(user_id=user_id).count()

    if todo_count > 0 or achievement_count > 0 or plan_count > 0:
        print(f"已存在示例数据 (待办事项: {todo_count}, 成就: {achievement_count}, 未来计划: {plan_count})")
        return

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
    create_test_data()
