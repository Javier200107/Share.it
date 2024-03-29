from backend.models.accounts import AccountsModel, auth, g
from backend.models.notifications import NotificationsModel
from backend.utils import lock
from flask_restful import Resource, reqparse


class Follow(Resource):
    @auth.login_required()
    def get(self, account1, account2=None):
        if not account2:
            acc2 = g.user
        else:
            acc2 = AccountsModel.get_by_username(account2)
        acc1 = AccountsModel.get_by_username(account1)
        if acc1 and acc2:
            follows = acc1.followers
            if follows:
                for i in follows:
                    if i.id == acc2.id:
                        return {"message": "Account1 [{}] follows Account2 [{}]".format(account1, account2)}, 200
                return {"message": "Account1 [{}] doesn't follow Account2 [{}]".format(account1, account2)}, 404
            else:
                return {"message": "Account [{}] doesn't follow any account".format(account1)}, 404
        else:
            return {"message": "Account [{}] or [{}] doesn't exist".format(account1, account2)}, 404

    @auth.login_required()
    def post(self, account1, account2=None):
        acc1 = AccountsModel.get_by_username(account1)
        if not account2:
            acc2 = g.user
        else:
            acc2 = AccountsModel.get_by_username(account2)
        if acc1 and acc2:
            follow = acc1.followers
            following = acc2.following
            if acc1.id == acc2.id:
                return {"message": "An account cannot follow itself"}, 404
            if follow:
                for i in follow:
                    if i.id == acc2.id:
                        # es podria fer que si ja el segueix el deixi de seguir
                        return {
                            "message": "Account1 [{}] already follows Account2 [{}]".format(account1, account2)
                        }, 404
            follow.append(acc2)
            noti = NotificationsModel(0)
            noti.account_id2 = acc2.id
            noti.account_id = acc1.id
            try:
                noti.save_to_db()
            except:
                noti.rollback()
                return {"message": "An error occurred inserting the Follow-Notification."}, 500
            try:
                # acc1.save_to_db()
                acc2.save_to_db()
                return {"Account": acc1.json()}, 200
            except:
                # acc1.rollback()
                acc2.rollback()
                return {"message": "An error occurred inserting the Follow."}, 500
        else:
            return {"message": "Account1 [{}] or Account2 [{}] doesn't exist".format(account1, account2)}, 404

    @auth.login_required()
    def delete(self, account1, account2=None):
        with lock.lock:
            acc1 = AccountsModel.get_by_username(account1)
            if not account2:
                acc2 = g.user
            else:
                acc2 = AccountsModel.get_by_username(account2)
            if acc1 and acc2:
                follow = acc1.followers
                following = acc2.following
                if follow:
                    for i in follow:
                        if i.id == acc2.id:
                            follow.remove(i)
                            try:
                                #   acc1.save_to_db()
                                acc2.save_to_db()
                                return {"Account": acc1.json()}, 200
                            except:
                                #  acc1.rollback()
                                acc2.rollback()
                                return {"message": "An error occurred deleting the Follow."}, 500
                    return {"message": "Follow with [{}] and [{}] doesn't exist".format(account1, account2)}, 404
                else:
                    return {"message": "Account [{}] doesn't have follows".format(account1)}, 404
            else:
                return {"message": "Account1 [{}] or Account2 [{}] doesn't exist".format(account1, account2)}, 404


class ListFollows(Resource):
    @auth.login_required()
    def get(self, account=None):
        if account is None:
            acc = g.user
        else:
            acc = AccountsModel.get_by_username(account)
        if acc:
            return {"ListFollows": [f.json() for f in acc.followers]}, 200
        else:
            return {"message": "Account [{}] doesn't exist".format(account)}, 404


class ListFollowing(Resource):
    @auth.login_required()
    def get(self, account=None):
        if account is None:
            acc = g.user
        else:
            acc = AccountsModel.get_by_username(account)
        if acc:
            return {"ListFollowing": [f.json() for f in acc.following]}, 200
        else:
            return {"message": "Account [{}] doesn't exist".format(account)}, 404


class PostsFollowing(Resource):
    @auth.login_required()
    def get(self, user=None):
        parser = reqparse.RequestParser()
        parser.add_argument("limit", type=int, required=True, nullable=False, location="args")
        parser.add_argument("offset", type=int, required=True, nullable=False, location="args")
        data = parser.parse_args()
        if user is None:
            us = g.user
        else:
            us = AccountsModel.get_by_username(user)
        if us:
            posts = us.followed_posts_and_self(data["limit"], data["offset"])
            if posts:
                return {"posts": [post.json() for post in posts]}, 200
            else:
                return {"message": "No posts were found"}, 404
        else:
            return {"message": "User not found"}, 404
