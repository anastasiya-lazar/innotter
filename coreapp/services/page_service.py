from django.utils import timezone
from coreapp.services.exceptions import UserNotFoundException
from django.shortcuts import get_object_or_404


class PageService:
    def page_follow_unfollow(self, page, user, validated_data):
        if validated_data["follow"]:
            if page.is_private:
                page.follow_requests.add(user)
            else:
                page.followers.add(user)
        else:
            if page.is_private:
                page.follow_requests.remove(user)
                page.followers.remove(user)
            else:
                page.followers.remove(user)
        return page

    def accept_decline_follow_requests(self, validated_data, user_id, page):
        if user_id:
            user = get_object_or_404(page.follow_requests, id=user_id)
            page.follow_requests.remove(user)
            if validated_data["accept"]:
                page.followers.add(user)
        else:
            if validated_data["accept"]:
                users = page.follow_requests.all()
                if users:
                    page.followers.add(*users)
                page.follow_requests.clear()
            else:
                page.follow_requests.clear()
        return page

    def clear_unblock_date(self, obj):
        if obj.unblock_date <= timezone.now():
            obj.unblock_date = None
            obj.save()
