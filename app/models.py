from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    nickname = models.CharField(max_length=20, default=None, unique=True)
    avatar = models.ImageField(blank=False, null=True)

class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, blank=True)

    def __unicode__(self):
        return self.title

class Answer(models.Model):
    text = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

class Rating(models.Model):
    like = 1
    dislike = -1
    rating_choices = (
        (like, 'like'),
        (dislike, 'dislike')
    )

    value = models.IntegerField(choices=rating_choices)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, blank=True, null=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, blank=True, null=True, on_delete=models.CASCADE)
