from coreapp.services.exceptions import UserNotFoundException
from coreapp.models import User
from django.utils import timezone


def page_follow_unfollow(page, user, validated_data):
    if validated_data['follow']:
        if page.is_private:
            page.follow_requests.add(user)
        else:
            page.followers.add(user)
    else:
        if page.is_private:
            try:
                follower = page.follow_requests.get(id=user.id)
                page.follow_requests.remove(follower)
            except User.DoesNotExist:
                try:
                    page.followers.get(id=user.id)
                    page.followers.remove(user)
                except User.DoesNotExist:
                    raise UserNotFoundException
        else:
            if page.followers.get(id=user.id):
                page.followers.remove(user)
    return page


def accept_decline_follow_requests(validated_data, page):
    if validated_data['user_id']:
        user = page.follow_requests.get(id=validated_data['user_id'])
        if user:
            if validated_data["accept"]:
                page.followers.add(user)
                page.follow_requests.remove(user)
            else:
                page.follow_requests.remove(user)
    else:
        if validated_data["accept"]:
            users = page.follow_requests.all()
            if users:
                for user in users:
                    page.followers.add(user)
                    page.follow_requests.clear()
        else:
            page.follow_requests.clear()
    return page


def clear_unblock_date(obj):
    if obj.unblock_date <= timezone.now():
        obj.unblock_date = None
        obj.save()
