class PostService:
    def like_or_unlike(self, post, validated_data, user):
        if validated_data["to_like"]:
            post.likes.add(user)
        else:
            post.likes.remove(user)
        return post

    def add_likes(self, post, validated_data, request):
        user = request.user
        like_post = self.like_or_unlike(post, validated_data, user)
        validated_data.pop("to_like", None)
        return like_post
