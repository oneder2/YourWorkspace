# /your_project_root/app/api/blog_bp.py
# Blueprint for blog post related API endpoints (CRUD operations).

from flask import Blueprint, jsonify, request
# Import necessary components later (e.g., Post model, schemas, db session, JWT decorator)
# from ...models.post import Post
# from ...schemas.post_schema import PostSchema # Example using Marshmallow
# from ...extensions import db
# from flask_jwt_extended import jwt_required, get_jwt_identity

# Create a Blueprint instance named 'blog'
blog_bp = Blueprint('blog', __name__)

# --- Placeholder Data (Remove when using database) ---
_posts = {
    1: {"id": 1, "title": "First Post", "content": "This is the content of the first post.", "author_id": 1},
    2: {"id": 2, "title": "Second Post", "content": "Some interesting thoughts here.", "author_id": 1},
    3: {"id": 3, "title": "Another Author's Post", "content": "Content by someone else.", "author_id": 2},
}
_next_post_id = 4

# --- Blog Post Routes ---

@blog_bp.route('/ping', methods=['GET'])
def ping_blog():
    """Simple test route."""
    return jsonify({"message": "Blog API is alive!"}), 200

@blog_bp.route('/posts', methods=['GET'])
def get_posts():
    """
    Endpoint to retrieve a list of all blog posts.
    Add pagination later.
    """
    # --- Add logic to fetch posts from database ---
    # Example with SQLAlchemy and Marshmallow:
    # posts = Post.query.order_by(Post.created_at.desc()).all()
    # post_schema = PostSchema(many=True)
    # return jsonify(post_schema.dump(posts)), 200

    # Placeholder response:
    return jsonify(list(_posts.values())), 200


@blog_bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """
    Endpoint to retrieve a single blog post by its ID.
    """
    # --- Add logic to fetch a single post from database ---
    # Example:
    # post = Post.query.get_or_404(post_id)
    # post_schema = PostSchema()
    # return jsonify(post_schema.dump(post)), 200

    # Placeholder response:
    post = _posts.get(post_id)
    if post:
        return jsonify(post), 200
    else:
        return jsonify({"error": "Post not found"}), 404


@blog_bp.route('/posts', methods=['POST'])
#@jwt_required() # Protect this route: only logged-in users can create posts
def create_post():
    """
    Endpoint to create a new blog post.
    Expects JSON data: {'title': '...', 'content': '...'}
    Associates the post with the currently logged-in user.
    """
    data = request.get_json()
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({"error": "Missing required fields (title, content)"}), 400

    # --- Add logic to create a post in the database ---
    # Example:
    # current_user_id = get_jwt_identity()
    # new_post = Post(title=data['title'], content=data['content'], author_id=current_user_id)
    # db.session.add(new_post)
    # db.session.commit()
    # post_schema = PostSchema()
    # return jsonify(post_schema.dump(new_post)), 201

    # Placeholder response:
    global _next_post_id
    # current_user_id = get_jwt_identity() # Would fail without @jwt_required
    current_user_id = 1 # Placeholder user ID
    new_post_data = {
        "id": _next_post_id,
        "title": data['title'],
        "content": data['content'],
        "author_id": current_user_id
    }
    _posts[_next_post_id] = new_post_data
    _next_post_id += 1
    return jsonify(new_post_data), 201


@blog_bp.route('/posts/<int:post_id>', methods=['PUT'])
#@jwt_required()
def update_post(post_id):
    """
    Endpoint to update an existing blog post.
    Expects JSON data: {'title': '...', 'content': '...'}
    Only the author of the post should be allowed to update it.
    """
    data = request.get_json()
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({"error": "Missing required fields (title, content)"}), 400

    # --- Add logic to update a post in the database ---
    # Example:
    # post = Post.query.get_or_404(post_id)
    # current_user_id = get_jwt_identity()
    # if post.author_id != current_user_id:
    #     return jsonify({"error": "Forbidden: You cannot edit this post"}), 403
    #
    # post.title = data['title']
    # post.content = data['content']
    # db.session.commit()
    # post_schema = PostSchema()
    # return jsonify(post_schema.dump(post)), 200

    # Placeholder response:
    post = _posts.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    # current_user_id = get_jwt_identity() # Would fail without @jwt_required
    current_user_id = 1 # Placeholder user ID
    if post['author_id'] != current_user_id:
         return jsonify({"error": "Forbidden: You cannot edit this post"}), 403

    post['title'] = data['title']
    post['content'] = data['content']
    return jsonify(post), 200


@blog_bp.route('/posts/<int:post_id>', methods=['DELETE'])
#@jwt_required()
def delete_post(post_id):
    """
    Endpoint to delete a blog post.
    Only the author of the post should be allowed to delete it.
    """
    # --- Add logic to delete a post from the database ---
    # Example:
    # post = Post.query.get_or_404(post_id)
    # current_user_id = get_jwt_identity()
    # if post.author_id != current_user_id:
    #     return jsonify({"error": "Forbidden: You cannot delete this post"}), 403
    #
    # db.session.delete(post)
    # db.session.commit()
    # return '', 204 # No Content response

    # Placeholder response:
    post = _posts.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    # current_user_id = get_jwt_identity() # Would fail without @jwt_required
    current_user_id = 1 # Placeholder user ID
    if post['author_id'] != current_user_id:
         return jsonify({"error": "Forbidden: You cannot delete this post"}), 403

    del _posts[post_id]
    return '', 204 # No Content
