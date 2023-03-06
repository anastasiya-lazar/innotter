from coreapp.models import User
from rest_framework.exceptions import APIException


def like_or_unlike(post, validated_data, user):
    if validated_data['to_like']:
        post.likes.add(user)
    else:
        try:
            user_like = post.likes.get(id=user.id)
            post.likes.remove(user_like)
        except User.DoesNotExist:
            raise APIException("You can not unlike post")
    return post
