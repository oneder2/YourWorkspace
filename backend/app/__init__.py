# /your_project_root/app/__init__.py
# 经过修改，用于同时服务后端 API 和 Svelte 前端静态文件

from flask import Flask, send_from_directory
from flask_cors import CORS
import os

# 导入配置和所有扩展，这些都保持原样
from .config import config
from .extensions import db, migrate, bcrypt, jwt

def create_app(config_name='development'):
    """
    应用工厂函数。
    """
    # --- 主要改动 1: 修改 Flask 实例的创建 ---
    # 我们添加了 static_folder 和 static_url_path 参数。
    # static_folder='../static' 告诉 Flask 静态文件存放在上级目录的 'static' 文件夹中。
    # static_url_path=None 禁用Flask的自动静态文件路由，我们将手动处理。
    app = Flask(__name__,
                instance_relative_config=True,
                static_folder='../static',
                static_url_path=None)

    # --- 加载配置 (原封不动) ---
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # --- 初始化所有扩展 (原封不动) ---
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # --- 注册所有 API 蓝图 (原封不动) ---
    # 因为您的所有API路由都有 /api/v1 前缀，所以它们不会和前端路由冲突。
    from .api.auth_bp import auth_bp
    from .api.anchor_bp import anchor_bp
    from .api.todo_bp import todo_bp
    from .api.achievements_bp import achievements_bp
    from .api.plans_bp import plans_bp
    from .api.blog_bp import blog_bp
    from .api.ai_bp import ai_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(blog_bp, url_prefix='/blog')
    app.register_blueprint(todo_bp, url_prefix='/todo')
    app.register_blueprint(ai_bp, url_prefix='/ai')
    app.register_blueprint(anchor_bp, url_prefix='/anchor')
    app.register_blueprint(achievements_bp, url_prefix='/achievements')
    app.register_blueprint(plans_bp, url_prefix='/plans')

    # --- 数据库创建部分 (原封不动) ---
    # with app.app_context():
    #     from . import models
    #     db.create_all()

    # --- 主要改动 2: 添加服务前端的路由 ---
    # 我们用下面的路由逻辑替换了原来简单的 @app.route('/')
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        """
        这个路由是核心。它负责两件事：
        1. 如果请求的路径是一个存在于 static 文件夹中的真实文件 (例如 /favicon.png, /_app/...),
           Flask 的静态文件处理会自动提供它。
        2. 如果请求的路径不是一个真实的文件 (例如 /login, /doing, /done, /plan, 这是 Svelte 的前端路由),
           我们就返回前端的主入口 index.html。浏览器加载 index.html 后，Svelte Router 就会接管，
           并根据 URL 显示正确的页面。
        """
        # 检查是否是静态文件
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            # 对于所有其他路径（包括前端路由），返回 index.html
            return send_from_directory(app.static_folder, 'index.html')

    return app