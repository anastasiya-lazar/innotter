from coreapp.models import User
import datetime


def change_user_status(user, role):
    if role == User.Roles.MODERATOR:
        user.is_staff = True
        user.is_superuser = False
    elif role == User.Roles.ADMIN:
        user.is_staff = True
        user.is_superuser = True
    elif role == User.Roles.USER:
        user.is_staff = False
        user.is_superuser = False
    user.save()


def block_users_pages(user, serializer):
    if serializer.data['is_blocked']:
        pages = user.pages.all()
        if pages:
            for page in pages:
                print(datetime.timedelta.max)
                page.unblock_date = datetime.datetime.max
                page.save()
    else:
        pages = user.pages.all()
        if pages:
            for page in pages:
                page.unblock_date = None
                page.save()
