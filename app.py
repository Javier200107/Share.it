from backend.config import environment
from backend.db import db
from backend.resources.accounts import Accounts
from backend.resources.follow import Follow, ListFollowing, ListFollows, PostsFollowing
from backend.resources.like import Like, ListPostLikes, ListUserLikes
from backend.resources.login import Login
from backend.resources.posts import Posts, UserPosts
from flask import Flask, render_template
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api

app = Flask(__name__)
app.config.from_object(environment)
db.init_app(app)
Migrate(app, db)

print(
    f"-> PRODUCTION={app.config['PRODUCTION']}, RECREATE_DB_ON_STARTUP={app.config['RECREATE_DB_ON_STARTUP']}"
)

if app.config["RECREATE_DB_ON_STARTUP"]:
    with app.app_context():
        db.drop_all()
        db.create_all()
        # TODO: init with some data

api = Api(app)
CORS(app, resources={r"/*": {"origins": "*"}})

api.add_resource(Accounts, "/account/<string:username>", "/account")
api.add_resource(Login, "/login")
api.add_resource(Posts, "/posts/<int:id>", "/posts")
api.add_resource(UserPosts, "/uposts/<string:user>", "/uposts")
api.add_resource(Like, "/likes/<string:account>,<int:post>", "/likes/<int:post>")
api.add_resource(ListPostLikes, "/likePlist/<int:postid>")
api.add_resource(ListUserLikes, "/likeUlist/<int:userid>", "/likeUlist/")

api.add_resource(
    Follow, "/follow/<string:account1>/<string:account2>", "/follow/<string:account1>"
)
api.add_resource(ListFollows, "/followList/<string:account>", "/followList/")
api.add_resource(ListFollowing, "/followingList/<string:account>", "/followingList/")
api.add_resource(PostsFollowing, "/followingPosts/", "/followingPosts/<string:user>")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
