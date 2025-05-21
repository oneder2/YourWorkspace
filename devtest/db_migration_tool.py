#!/usr/bin/env python3
"""
数据库迁移工具
此脚本用于在PostgreSQL和SQLite之间迁移数据，确保两种数据库具有相同的表结构和数据。
"""

import os
import sys
import json
import datetime
import argparse
from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker

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

# 颜色常量，用于终端输出
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(message):
    """打印格式化的标题消息"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{message.center(80)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}\n")

def print_info(message):
    """打印信息消息"""
    print(f"{Colors.OKBLUE}[INFO]{Colors.ENDC} {message}")

def print_success(message):
    """打印成功消息"""
    print(f"{Colors.OKGREEN}[SUCCESS]{Colors.ENDC} {message}")

def print_warning(message):
    """打印警告消息"""
    print(f"{Colors.WARNING}[WARNING]{Colors.ENDC} {message}")

def print_error(message):
    """打印错误消息"""
    print(f"{Colors.FAIL}[ERROR]{Colors.ENDC} {message}")

def get_db_url(db_type):
    """获取数据库URL"""
    if db_type == 'postgres':
        # 从环境变量获取PostgreSQL连接信息
        pg_host = os.environ.get('POSTGRES_HOST', 'localhost')
        pg_port = os.environ.get('POSTGRES_PORT', '5432')
        pg_user = os.environ.get('POSTGRES_USER', 'postgres')
        pg_password = os.environ.get('POSTGRES_PASSWORD', '')
        pg_db = os.environ.get('POSTGRES_DB_DEV', 'mydatabase')

        return f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"
    elif db_type == 'sqlite':
        # 使用SQLite数据库
        instance_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
        if not os.path.exists(instance_dir):
            os.makedirs(instance_dir)

        return f"sqlite:///{os.path.join(instance_dir, 'dev.sqlite')}"
    else:
        raise ValueError(f"不支持的数据库类型: {db_type}")

def init_db(db_type):
    """初始化数据库"""
    print_header(f"初始化{db_type.upper()}数据库")

    # 创建Flask应用实例
    app = create_app('development')

    # 更新数据库URL
    app.config['SQLALCHEMY_DATABASE_URI'] = get_db_url(db_type)

    # 创建数据库表
    with app.app_context():
        db.create_all()
        print_success("数据库表创建完成")

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
            print_success("测试用户创建完成")

            # 创建示例数据
            create_sample_data(test_user.id)
        else:
            print_info(f"测试用户已存在 (ID: {test_user.id})")

            # 检查是否需要创建示例数据
            todo_count = TodoItem.query.filter_by(user_id=test_user.id).count()
            achievement_count = Achievement.query.filter_by(user_id=test_user.id).count()
            plan_count = FuturePlan.query.filter_by(user_id=test_user.id).count()

            if todo_count == 0 and achievement_count == 0 and plan_count == 0:
                print_info("未找到示例数据，正在创建...")
                create_sample_data(test_user.id)
            else:
                print_info(f"已存在示例数据 (待办事项: {todo_count}, 成就: {achievement_count}, 未来计划: {plan_count})")

        print_success(f"{db_type.upper()}数据库初始化完成")

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
    print_success(f"创建了 {len(todos)} 个示例待办事项")

    # 创建示例成就
    achievements = [
        Achievement(
            user_id=user_id,
            title="完成前端开发课程",
            description="完成了现代前端开发的综合课程。",
            date_achieved="2023-01-15",
            core_skills_json=["HTML", "CSS", "JavaScript", "React"]
        ),
        Achievement(
            user_id=user_id,
            title="发布第一个Web应用",
            description="成功将第一个Web应用部署到生产环境。",
            date_achieved="2023-03-20",
            core_skills_json=["Node.js", "Express", "MongoDB", "Deployment"]
        )
    ]

    db.session.add_all(achievements)
    db.session.commit()
    print_success(f"创建了 {len(achievements)} 个示例成就")

    # 创建示例未来计划
    plans = [
        FuturePlan(
            user_id=user_id,
            title="学习机器学习",
            description="完成机器学习基础课程。",
            goal_type="learning",
            target_date="2023-12-31",
            status="active"
        ),
        FuturePlan(
            user_id=user_id,
            title="构建移动应用",
            description="开发并发布一个移动应用。",
            goal_type="project",
            target_date="2024-06-30",
            status="active"
        )
    ]

    db.session.add_all(plans)
    db.session.commit()
    print_success(f"创建了 {len(plans)} 个示例未来计划")

def export_data(db_type, output_file):
    """从数据库导出数据到JSON文件"""
    print_header(f"从{db_type.upper()}导出数据")

    # 创建Flask应用实例
    app = create_app('development')

    # 更新数据库URL
    app.config['SQLALCHEMY_DATABASE_URI'] = get_db_url(db_type)

    data = {
        'users': [],
        'user_profiles': [],
        'todo_items': [],
        'achievements': [],
        'future_plans': [],
        'token_blocklist': []
    }

    with app.app_context():
        # 导出用户数据
        users = User.query.all()
        for user in users:
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'password_hash': user.password_hash,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'updated_at': user.updated_at.isoformat() if user.updated_at else None
            }
            data['users'].append(user_data)

        # 导出用户配置文件数据
        profiles = UserProfile.query.all()
        for profile in profiles:
            profile_data = {
                'id': profile.id,
                'professional_title': profile.professional_title,
                'one_liner_bio': profile.one_liner_bio,
                'skill': profile.skill,
                'summary': profile.summary,
                'created_at': profile.created_at.isoformat() if profile.created_at else None,
                'updated_at': profile.updated_at.isoformat() if profile.updated_at else None
            }
            data['user_profiles'].append(profile_data)

        # 导出待办事项数据
        todos = TodoItem.query.all()
        for todo in todos:
            todo_data = {
                'id': todo.id,
                'user_id': todo.user_id,
                'title': todo.title,
                'description': todo.description,
                'due_date': todo.due_date.isoformat() if todo.due_date else None,
                'status': todo.status,
                'priority': todo.priority,
                'is_current_focus': todo.is_current_focus,
                'created_at': todo.created_at.isoformat() if todo.created_at else None,
                'updated_at': todo.updated_at.isoformat() if todo.updated_at else None,
                'completed_at': todo.completed_at.isoformat() if todo.completed_at else None
            }
            data['todo_items'].append(todo_data)

        # 导出成就数据
        achievements = Achievement.query.all()
        for achievement in achievements:
            achievement_data = {
                'id': achievement.id,
                'user_id': achievement.user_id,
                'title': achievement.title,
                'description': achievement.description,
                'quantifiable_results': achievement.quantifiable_results,
                'core_skills_json': achievement.core_skills_json,
                'date_achieved': achievement.date_achieved.isoformat() if achievement.date_achieved else None,
                'created_at': achievement.created_at.isoformat() if achievement.created_at else None,
                'updated_at': achievement.updated_at.isoformat() if achievement.updated_at else None
            }
            data['achievements'].append(achievement_data)

        # 导出未来计划数据
        plans = FuturePlan.query.all()
        for plan in plans:
            plan_data = {
                'id': plan.id,
                'user_id': plan.user_id,
                'goal_type': plan.goal_type,
                'title': plan.title,
                'description': plan.description,
                'target_date': plan.target_date.isoformat() if plan.target_date else None,
                'status': plan.status,
                'created_at': plan.created_at.isoformat() if plan.created_at else None,
                'updated_at': plan.updated_at.isoformat() if plan.updated_at else None
            }
            data['future_plans'].append(plan_data)

        # 导出令牌黑名单数据
        tokens = TokenBlocklist.query.all()
        for token in tokens:
            token_data = {
                'id': token.id,
                'jti': token.jti,
                'token_type': token.token_type,
                'user_id': token.user_id,
                'created_at': token.created_at.isoformat() if token.created_at else None
            }
            data['token_blocklist'].append(token_data)

    # 将数据写入JSON文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print_success(f"数据已导出到 {output_file}")
    return data

def import_data(db_type, input_file):
    """从JSON文件导入数据到数据库"""
    print_header(f"导入数据到{db_type.upper()}")

    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print_error(f"输入文件不存在: {input_file}")
        return False

    # 从JSON文件加载数据
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 创建Flask应用实例
    app = create_app('development')

    # 更新数据库URL
    app.config['SQLALCHEMY_DATABASE_URI'] = get_db_url(db_type)

    with app.app_context():
        # 清空现有数据
        print_info("清空现有数据...")
        db.session.query(TokenBlocklist).delete()
        db.session.query(Achievement).delete()
        db.session.query(FuturePlan).delete()
        db.session.query(TodoItem).delete()
        db.session.query(UserProfile).delete()
        db.session.query(User).delete()
        db.session.commit()

        # 导入用户数据
        print_info(f"导入 {len(data['users'])} 个用户...")
        for user_data in data['users']:
            user = User(
                id=user_data['id'],
                username=user_data['username'],
                email=user_data['email']
            )
            user.password_hash = user_data['password_hash']
            if user_data['created_at']:
                user.created_at = datetime.datetime.fromisoformat(user_data['created_at'])
            if user_data['updated_at']:
                user.updated_at = datetime.datetime.fromisoformat(user_data['updated_at'])
            db.session.add(user)

        # 提交用户数据，以便后续导入可以引用用户ID
        db.session.commit()

        # 导入用户配置文件数据
        print_info(f"导入 {len(data['user_profiles'])} 个用户配置文件...")
        for profile_data in data['user_profiles']:
            # 检查用户是否已经有配置文件（通过User.__init__自动创建）
            profile = UserProfile.query.get(profile_data['id'])
            if profile:
                # 更新现有配置文件
                profile.professional_title = profile_data['professional_title']
                profile.one_liner_bio = profile_data['one_liner_bio']
                profile.skill = profile_data['skill']
                profile.summary = profile_data['summary']
                if profile_data['created_at']:
                    profile.created_at = datetime.datetime.fromisoformat(profile_data['created_at'])
                if profile_data['updated_at']:
                    profile.updated_at = datetime.datetime.fromisoformat(profile_data['updated_at'])
            else:
                # 创建新配置文件
                profile = UserProfile(
                    id=profile_data['id'],
                    professional_title=profile_data['professional_title'],
                    one_liner_bio=profile_data['one_liner_bio'],
                    skill=profile_data['skill'],
                    summary=profile_data['summary']
                )
                if profile_data['created_at']:
                    profile.created_at = datetime.datetime.fromisoformat(profile_data['created_at'])
                if profile_data['updated_at']:
                    profile.updated_at = datetime.datetime.fromisoformat(profile_data['updated_at'])
                db.session.add(profile)

        db.session.commit()

        # 导入待办事项数据
        print_info(f"导入 {len(data['todo_items'])} 个待办事项...")
        for todo_data in data['todo_items']:
            todo = TodoItem(
                id=todo_data['id'],
                user_id=todo_data['user_id'],
                title=todo_data['title'],
                description=todo_data['description'],
                status=todo_data['status'],
                priority=todo_data['priority'],
                is_current_focus=todo_data['is_current_focus']
            )
            if todo_data['due_date']:
                todo.due_date = datetime.date.fromisoformat(todo_data['due_date'])
            if todo_data['created_at']:
                todo.created_at = datetime.datetime.fromisoformat(todo_data['created_at'])
            if todo_data['updated_at']:
                todo.updated_at = datetime.datetime.fromisoformat(todo_data['updated_at'])
            if todo_data['completed_at']:
                todo.completed_at = datetime.datetime.fromisoformat(todo_data['completed_at'])
            db.session.add(todo)

        # 导入成就数据
        print_info(f"导入 {len(data['achievements'])} 个成就...")
        for achievement_data in data['achievements']:
            achievement = Achievement(
                id=achievement_data['id'],
                user_id=achievement_data['user_id'],
                title=achievement_data['title'],
                description=achievement_data['description'],
                quantifiable_results=achievement_data['quantifiable_results'],
                core_skills_json=achievement_data['core_skills_json']
            )
            if achievement_data['date_achieved']:
                achievement.date_achieved = datetime.date.fromisoformat(achievement_data['date_achieved'])
            if achievement_data['created_at']:
                achievement.created_at = datetime.datetime.fromisoformat(achievement_data['created_at'])
            if achievement_data['updated_at']:
                achievement.updated_at = datetime.datetime.fromisoformat(achievement_data['updated_at'])
            db.session.add(achievement)

        # 导入未来计划数据
        print_info(f"导入 {len(data['future_plans'])} 个未来计划...")
        for plan_data in data['future_plans']:
            plan = FuturePlan(
                id=plan_data['id'],
                user_id=plan_data['user_id'],
                goal_type=plan_data['goal_type'],
                title=plan_data['title'],
                description=plan_data['description'],
                status=plan_data['status']
            )
            if plan_data['target_date']:
                plan.target_date = datetime.date.fromisoformat(plan_data['target_date'])
            if plan_data['created_at']:
                plan.created_at = datetime.datetime.fromisoformat(plan_data['created_at'])
            if plan_data['updated_at']:
                plan.updated_at = datetime.datetime.fromisoformat(plan_data['updated_at'])
            db.session.add(plan)

        # 导入令牌黑名单数据
        print_info(f"导入 {len(data['token_blocklist'])} 个令牌黑名单项...")
        for token_data in data['token_blocklist']:
            token = TokenBlocklist(
                id=token_data['id'],
                jti=token_data['jti'],
                token_type=token_data['token_type'],
                user_id=token_data['user_id']
            )
            if token_data['created_at']:
                token.created_at = datetime.datetime.fromisoformat(token_data['created_at'])
            db.session.add(token)

        # 提交所有更改
        db.session.commit()

    print_success(f"数据已成功导入到{db_type.upper()}数据库")
    return True

def migrate_data(source_db, target_db, data_file=None):
    """将数据从一个数据库迁移到另一个数据库"""
    print_header(f"将数据从{source_db.upper()}迁移到{target_db.upper()}")

    # 如果没有提供数据文件，则使用临时文件
    if data_file is None:
        data_file = f"temp_migration_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    # 从源数据库导出数据
    data = export_data(source_db, data_file)

    # 将数据导入目标数据库
    success = import_data(target_db, data_file)

    if success:
        print_success(f"数据已成功从{source_db.upper()}迁移到{target_db.upper()}")
    else:
        print_error(f"数据迁移失败")

    # 如果使用临时文件，则删除它
    if data_file.startswith("temp_migration_") and os.path.exists(data_file):
        os.remove(data_file)
        print_info(f"临时数据文件已删除: {data_file}")

    return success

def check_db_connection(db_type):
    """检查数据库连接"""
    print_header(f"检查{db_type.upper()}数据库连接")

    try:
        # 获取数据库URL
        db_url = get_db_url(db_type)

        # 创建引擎
        engine = create_engine(db_url)

        # 尝试连接
        connection = engine.connect()
        connection.close()

        print_success(f"{db_type.upper()}数据库连接成功")
        return True
    except Exception as e:
        print_error(f"{db_type.upper()}数据库连接失败: {str(e)}")
        return False

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="数据库迁移工具")
    parser.add_argument("--action", choices=["init", "export", "import", "migrate", "check"], required=True,
                        help="要执行的操作: init(初始化), export(导出), import(导入), migrate(迁移), check(检查连接)")
    parser.add_argument("--source", choices=["postgres", "sqlite"], default="postgres",
                        help="源数据库类型 (默认: postgres)")
    parser.add_argument("--target", choices=["postgres", "sqlite"], default="sqlite",
                        help="目标数据库类型 (默认: sqlite)")
    parser.add_argument("--file", help="数据文件路径 (用于导出/导入操作)")

    args = parser.parse_args()

    if args.action == "init":
        # 初始化数据库
        if args.source == "postgres" and args.target == "sqlite":
            # 初始化两个数据库
            init_db("postgres")
            init_db("sqlite")
        else:
            # 初始化指定的数据库
            init_db(args.source)

    elif args.action == "export":
        # 导出数据
        if not args.file:
            args.file = f"{args.source}_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        export_data(args.source, args.file)

    elif args.action == "import":
        # 导入数据
        if not args.file:
            print_error("导入操作需要指定数据文件路径 (--file)")
            return
        import_data(args.target, args.file)

    elif args.action == "migrate":
        # 迁移数据
        migrate_data(args.source, args.target, args.file)

    elif args.action == "check":
        # 检查数据库连接
        check_db_connection(args.source)
        if args.source != args.target:
            check_db_connection(args.target)

if __name__ == "__main__":
    main()
