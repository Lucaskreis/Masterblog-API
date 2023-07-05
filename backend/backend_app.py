from flask import Flask, jsonify, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        abort(400, "Both 'title' and 'content' fields are required.")

    new_post = {
        "id": len(POSTS) + 1,
        "title": title,
        "content": content
    }
    POSTS.append(new_post)
    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    post = next((p for p in POSTS if p['id'] == post_id), None)
    if post is None:
        abort(404, f"Post with id {post_id} not found.")

    if title:
        post['title'] = title
    if content:
        post['content'] = content

    return jsonify(post)



@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = next((p for p in POSTS if p['id'] == post_id), None)
    if post:
        POSTS.remove(post)
        return jsonify({"message": f"Post with id {post_id} has been deleted successfully."})
    else:
        abort(404, f"Post with id {post_id} not found.")


@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": str(error)}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": str(error)}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
