from django.contrib import admin

# Register your models here.
from .models import Article


class ArticleModelAdmin(admin.ModelAdmin):
    list_display = ["article_id","title", "sentiment_type", "sentiment_score"]

    class Meta:
        model = Article


admin.site.register(Article, ArticleModelAdmin)