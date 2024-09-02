from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

def ordered_posts(parameter):
    # This function allows to order the posts using the parameter as reference, and return a list of posts ordered
    ordered_posts_list = []
    object_list = []
    for post in POSTS:
        object_list.append(post[parameter])
    object_list.sort()
    for object in object_list:
        for post in POSTS:
            if object == post[parameter]:
                ordered_posts_list.append(post)
    return ordered_posts_list

@app.route('/api/posts', methods=['GET'])
def get_posts():
    """""
    this function gets the posts in list with the ability to input a query
    if the user wants to list the posts in order either by content or by title
    """""
    if request.method == 'GET':
        sorted = request.args.get("sorted")
        direction = request.args.get("direction")
        if sorted == "title" or sorted == "content":
            if direction == "asc" or direction == "dsc":
                ordered_posts_list = ordered_posts(sorted)
                if direction == "asc":
                    return jsonify(ordered_posts_list)
                elif direction == "dsc":
                    return jsonify(ordered_posts_list[::-1])
            else:
                return jsonify("error: direction is not correct"), 400
        elif sorted == None:
            return jsonify(POSTS)
        else:
            return jsonify("error: sorted not correct"), 400

app.route('/api/posts', methods=['POST'])
def add():
    """""
    This function add a new post to the posts list using a POST method
    to retrieve the data in json format  
    """""
    if request.method == 'POST':
        data = request.get_json()
        new_id = 0
        for post in POSTS:
            if post["id"] > new_id:
                new_id = post["id"]
        data["id"] = new_id + 1 # creating a new id for the new post, adding 1 to the highest existing id number
        if isinstance(data, dict):
            if "title" in data.keys() and "content" in data.keys():
                POSTS.append(data)
            else:
                return jsonify("Error: invalid data in one of the items"), 400
        else:
            return jsonify("error: input data not a dictionary"), 400

        return jsonify(data)


def delete(id):
    # With the given id value, the function deletes an existing post from the list
    for post in POSTS:
        if int(id) in post.values():
            if int(post["id"]) == int(id):
                POSTS.remove(post)
                return jsonify("message: post with id {id} has been deleted successfully.")
        else:
            return jsonify("error: no id found"), 404

@app.route('/api/posts/<id>', methods=['PUT'])
def update(id):

    # This function updates a post with the given id number, it updates the title or the content or both of them
   if request.method == 'PUT':
        data = request.get_json()
        for post in POSTS:
            if int(id) in post.values: # checking if the given id is on the posts list
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
                return jsonify("error: id not found"), 400

@app.route('/api/posts/search')
def search():
    # this function searches for a post by its title or its content using the query parameters
    # and returns a list of the search result
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
