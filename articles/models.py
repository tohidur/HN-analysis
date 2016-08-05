from __future__ import unicode_literals

from django.db import models
from django.conf import settings

# Create your models here.

class Article(models.Model):
	article_id = models.IntegerField()
	author_username = models.CharField(max_length=120)
	title = models.CharField(max_length=300)
	url = models.CharField(max_length=300, null=True)
	score = models.IntegerField()
	description = models.TextField(null=True)
	sentiment_type = models.CharField(max_length=100)
	sentiment_score = models.IntegerField()
	update = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __unicode__(self):
	    return self.title

	def __str__(self):
	    return self.title

	class Meta:
	    ordering = ["-timestamp", "-id"]