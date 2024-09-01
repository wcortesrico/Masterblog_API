from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    if request.method == 'GET':
        return jsonify(POSTS)

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












if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
