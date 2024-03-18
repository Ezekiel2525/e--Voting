from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    total_vote = models.IntegerField(default=0)
    voters = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.title

    

class CategoryItem(models.Model):
    title = models.CharField(max_length=200)
    total_vote = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='item')
    voters = models.ManyToManyField(User, blank=True)


    @property
    def percentage_vote(self):
        category_vote = self.category.total_vote
        item_vote = self.total_vote
        if category_vote == 0:
            vote_in_percentage = 0
        else:
            vote_in_percentage = (item_vote/category_vote) * 100
            
        return vote_in_percentage

    def __str__(self):
        return self.title