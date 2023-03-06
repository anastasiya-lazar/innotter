from rest_framework import permissions
from coreapp.services.page_service import clear_unblock_date


class PageModelPermission(permissions.BasePermission):
    """
       A class for Page Model which specifies permissions for all actions.
    """

    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        elif view.action == 'create':
            return request.user.is_authenticated and not request.user.is_blocked
        elif view.action in ('retrieve', 'partial_update', 'destroy', 'follow_and_unfollow_page',
                             'get_list_follow_requests', 'accept_or_decline_follow_requests',
                             'block_page'):
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if obj.unblock_date:
            clear_unblock_date(obj)
        if not obj.unblock_date:
            if view.action == 'retrieve':
                return True
            elif view.action == 'get_list_follow_requests':
                if obj.is_private:
                    return obj.owner == request.user
            elif view.action == 'accept_or_decline_follow_requests':
                if obj.is_private:
                    return obj.owner == request.user
            elif view.action == 'follow_and_unfollow_page':
                return request.user.is_authenticated and obj.owner != request.user
            elif view.action == 'partial_update':
                return obj.owner == request.user
        if view.action == 'destroy':
            return obj.owner == request.user
        elif view.action == 'block_page':
            return request.user.is_staff
        else:
            return False


class PostModelPermission(permissions.BasePermission):
    """
        A class for Post Model which specifies permissions for all actions.
    """

    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        elif view.action == 'create':
            return request.user.is_authenticated and not request.user.is_blocked
        elif view.action in ('like_and_unlike_post', 'retrieve', 'partial_update', 'destroy'):
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if obj.page.unblock_date:
            return False
        else:
            if view.action == 'retrieve' or view.action == 'like_and_unlike_post':
                return True
            elif view.action == 'partial_update':
                return obj == request.user
        if view.action == 'destroy':
            return obj == request.user or request.user.is_staff
        else:
            return False


class TagModelPermission(permissions.BasePermission):
    """
        A class for Tag Model which specifies permissions for all actions.
    """

    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        elif view.action == 'create':
            return request.user.is_authenticated and not request.user.is_blocked
        elif view.action == 'destroy':
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if view.action == 'destroy':
            return obj == request.user and not request.user.is_blocked or request.user.is_staff
        else:
            return False


class UserPermission(permissions.BasePermission):
    """
        A class for Page Model which specifies permissions for all actions except 'block_user' and 'change_user_role'.
    """

    def has_permission(self, request, view):
        if view.action == 'list' or view.action == 'create':
            return True
        elif view.action in ('list_of_liked_posts', 'retrieve', 'partial_update', 'destroy'):
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            if not obj.is_blocked or obj == request.user:
                return True
        if request.user.is_authenticated:
            if not request.user.is_blocked:
                if view.action == 'list_of_liked_posts' or view.action == 'partial_update':
                    return obj == request.user
        elif view.action == 'destroy':
            return obj == request.user
        else:
            return False
