from django.db import models

class UserType(models.TextChoices):
    owner = "owner" ,"owner"
    customer = "customer","customer"

class UserStatusType(models.TextChoices):
    free = "free" ,"free"
    paid = "paid","paid" 


class BronStatus(models.TextChoices):
    waiting = "waiting","waiting" 
    active = "active" ,"active"
    cancelled = "cancelled","cancelled" 
    completed = "completed","completed" 

class CancellerType(models.TextChoices):
    owner = "owner","owner" 
    customer = "customer" ,"customer"

class LikeType(models.TextChoices):
    like = "like","like" 
    dislike = "dislike" ,"dislike"

class CommentType(models.TextChoices):
    bad = "bad" ,"bad"  # yomon
    satisfactory = "satisfactory","satisfactory"  # qoniqarli
    good = "good" ,"good"  # yaxshi
    excellent = "excellent" ,"excellent"  # zo'r
    great = "great" ,"great"  # super