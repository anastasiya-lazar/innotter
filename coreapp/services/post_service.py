from coreapp.services.aws_ses_service import SESService


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

    def send_new_post_notification_email(self, post):
        page = post.page
        owner = page.owner
        followers = page.followers.all()
        for follower in followers:
            email = follower.email
            SESService().send_email(
                source='innotter001@gmail.com',
                destination='testreceiver901@gmail.com',
                subject="New Post Notification",
                text=f"Go check out new post by {owner}",
                html=f"<h1>Go check out new post by {owner} on page {page.name}!</h1>"
            )
