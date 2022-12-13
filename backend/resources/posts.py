from backend.models.notifications import NotificationsModel
from backend.utils import lock
from backend.models.accounts import AccountsModel, auth, g
from backend.models.posts import PostsModel
from flask_restful import Resource, reqparse


class Posts(Resource):
    @auth.login_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "limit",
            type=int,
            required=False,
            nullable=False,
            help={"Number of posts to retrieve"},
            location="args",
        )
        parser.add_argument(
            "offset",
            type=int,
            required=False,
            nullable=False,
            help={"Number of posts to skip"},
            location="args",
        )
        data = parser.parse_args()
        posts = PostsModel.get_groups(data["limit"], data["offset"])
        if posts:
            return {"posts": [post.json() for post in posts]}, 200
        return {"message": "No posts were found"}, 404

    @auth.login_required()
    def post(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "text", type=str, required=True, nullable=False, help={"Text of the post"}
        )
        parser.add_argument(
            "parent_id",
            type=int,
            required=False,
            nullable=True,
            help={"Parent of the post"},
        )
        data = parser.parse_args()

        with lock.lock:
            new_post = PostsModel(data["text"])
            acc = AccountsModel.get_by_username(g.user.username)
            new_post.account = acc
            parent_id = data["parent_id"]
            addN = False
            if parent_id != None:
                parent = PostsModel.get_by_id(parent_id)
                new_post.parent = parent
                if(parent.account_id!=acc.id):
                    noti = NotificationsModel(2)
                    noti.account_id2 = acc.id
                    noti.account_id = parent.account_id
                    noti.post_id = new_post.id #Retorna el comentari
                    try:

                        noti.save_to_db()
                    except Exception:
                        noti.rollback()
                        return {"message": "An error occurred with post-Notification"}, 500

            if (id):
                new_post.community = 1
            try:
                new_post.save_to_db()
            except Exception:
                return {"message": "An error occurred creating the post"}, 500
            return {"post": new_post.json()}, 201

    @auth.login_required()
    def put(self, id):
        with lock.lock:
            post = PostsModel.get_by_id(id)
            if post is None:
                return {"message": "No post was found"}, 404
            if post.account.username != g.user.username:
                return {"message": "Unauthorized!"}, 403

            parser = reqparse.RequestParser()
            parser.add_argument("text", type=str, required=False, nullable=False, default=post.text)
            parser.add_argument("parent_id", type=int, required=False, nullable=True, default=post.parent_id)
            parser.add_argument("archived", type=int, required=False, nullable=False, default=post.archived)
            parser.add_argument("community", type=int, required=False, nullable=False, default=post.community)
            data = parser.parse_args()

            try:
                post.text = data["text"]
                post.parent = PostsModel.get_by_id(data["parent_id"])
                post.archived = data["archived"]
                post.community = data["community"]
                post.save_to_db()
            except Exception:
                return {"message": "An error occurred updating the post"}, 500
            return {"message": "Post updated successfully!"}, 200

    @auth.login_required()
    def delete(self, id):
        post = PostsModel.get_by_id(id)
        if post is None:
            return {"message": "No post was found"}, 404
        if post.account.username != g.user.username:
            return {"message": "Unauthorized!"}, 403
        try:
            post.delete_from_db()
        except Exception:
            return {"message": "An error occurred deleting the post"}, 500
        return {"message": "Post deleted successfully!"}, 200


class UserPosts(Resource):
    @auth.login_required()
    def get(self, user=None):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "limit",
            type=int,
            required=False,
            nullable=False,
            default=100,
            location="args",
        )
        parser.add_argument(
            "offset",
            type=int,
            required=False,
            nullable=False,
            default=0,
            location="args",
        )
        parser.add_argument(
            "archived",
            type=int,
            required=False,
            nullable=True,
            default=None,
            location="args",
        )
        data = parser.parse_args()
        same = 0
        account = g.user if user is None else AccountsModel.get_by_username(user)
        if not account:
            return {"message": "User not found"}, 404
        if account.id != g.user.id:
            same = 1
            if data["archived"]:
                return {"message": "Archived posts can only be seen by the owner"}, 403

        posts = PostsModel.get_groups_by_account(
            account.id, data["limit"], data["offset"], data["archived"], same
        )
        if posts:
            return {"posts": [post.json() for post in posts]}, 200
        return {"message": "No posts were found"}, 404


class Comments(Resource):
    @auth.login_required()
    def get(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "limit",
            type=int,
            required=True,
            nullable=False,
            help={"Number of posts to retrieve"},
            location="args",
        )
        parser.add_argument(
            "offset",
            type=int,
            required=True,
            nullable=False,
            help={"Number of posts to skip"},
            location="args",
        )
        data = parser.parse_args()
        posts = PostsModel.get_comments(data["limit"], data["offset"], id)
        if posts:
            return {"comments": [post.json() for post in posts]}, 200
        return {"message": "No comments were found"}, 404


class Post(Resource):
    @auth.login_required()
    def get(self, id):
        post = PostsModel.get_by_id(id)
        if post is None:
            return {"message": "No post was found"}, 404
        return {"post": post.json()}, 200

