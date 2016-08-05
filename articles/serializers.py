from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):

	class Meta:
		model = Article
		fields = ('author_username', 'title', 'url', 'score', 'description', 'sentiment_type', 'sentiment_score')