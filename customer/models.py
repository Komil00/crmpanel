from main.choicetypes import *
from main.models import User,Service
# Create your models here.



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name="notifications")
    text = models.TextField()
    status = models.BooleanField()
    reg_date = models.DateTimeField(auto_now_add=True)


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name="likes")
    service = models.ForeignKey(Service, on_delete=models.CASCADE , related_name="service_likes")
    like_type = models.CharField(max_length=15, blank=True, choices=LikeType.choices)
    reg_date = models.DateTimeField(auto_now_add=True)



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name="comments")
    service = models.ForeignKey(Service, on_delete=models.CASCADE , related_name="comments")
    text = models.TextField()
    comment_type = models.CharField(max_length=15, blank=True, choices=CommentType.choices)
    reg_date = models.DateTimeField(auto_now_add=True)