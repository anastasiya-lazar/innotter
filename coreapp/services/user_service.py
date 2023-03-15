from coreapp.models import User, Page
import datetime


class UserService:
    def change_user_status(self, user, role):
        if role == User.Roles.MODERATOR:
            user.is_staff = True
            user.is_superuser = False
        elif role == User.Roles.ADMIN:
            user.is_staff = True
            user.is_superuser = True
        elif role == User.Roles.USER:
            user.is_staff = False
            user.is_superuser = False
        user.save(update_fields=["is_staff", "is_superuser"])

    def block_users_pages(self, user, serializer):
        if serializer.data["is_blocked"]:
            Page.objects.filter(owner=user).update(unblock_date=datetime.datetime.max)
        else:
            Page.objects.filter(owner=user).update(unblock_date=None)
