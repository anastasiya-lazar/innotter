def like_or_unlike(post, validated_data, user):
    if validated_data['to_like']:
        post.likes.add(user)
    else:
        post.likes.remove(user)
    return post
