from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    if request.method == 'GET':
        return jsonify(POSTS)



app.route('/api/posts', methods=['POST'])
def add():
    if request.method == 'POST':
        data = request.get_json()
        new_id = 0
        for post in POSTS:
            if post["id"] > new_id:
                new_id = post["id"]
        data["id"] = new_id + 1
        if isinstance(data, dict):
            if "title" in data.keys() and "content" in data.keys():
                POSTS.append(data)
            else:
                return jsonify({"Error: invalid data in one of the items"}), 400
        else:
            return jsonify({"error: input data not a dictionary"}), 400

        return jsonify(data)


def delete(id):
    for post in POSTS:
        if int(id) in post.values():
            if int(post["id"]) == int(id):
                POSTS.remove(post)
                return jsonify({"message": "Post with id {id} has been deleted successfully."})
        else:
            return jsonify({"error: no id found"}), 404

@app.route('/api/posts/<id>', methods=['PUT'])
def update(id):
    if request.method == 'PUT':
        data = request.get_json()
        for post in POSTS:
            if int(id) in post.values:
                if int(id) == int(post["id"]):
                    if "title" in data.keys():
                        post["title"] = data["title"]
                    else:
                        pass
                    if "content" in data.keys():
                        post["content"] = data["content"]
                    else:
                        pass
                return jsonify(post)
            else:
                return jsonify({"error: id not found"})

@app.route('/api/posts/search')
def search():
    search_result = []
    title = request.args.get("title")
    content = request.args.get("content")
    if title:
        if content:
            for post in POSTS:
                if title in post["title"] and content in post["content"]:
                    search_result.append(post)
        else:
            for post in POSTS:
                if title in post["title"]:
                    search_result.append(post)
    elif content:
        for post in POSTS:
            if content in post["content"]:
                search_result.append(post)
    return jsonify(search_result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
