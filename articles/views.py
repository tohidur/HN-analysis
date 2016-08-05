import os
import threading
from .models import Article
from django.http import HttpResponse, HttpResponseRedirect,Http404
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import unirest
# Create your views here.

def get_articles_list(request):
    """
    """
    query_list = Article.objects.all()
    context = {
    	'articles_list': query_list,
    }
    
    t = threading.Thread(target=fetch_top_articles)
    t.setDaemon(False)
    t.start()
    
    return HttpResponse('<h1>Done</h1>')
    # return render(request, "base.html", context)


def fetch_top_articles():
	top_articles_id = unirest.get("https://community-hacker-news-v1.p.mashape.com/topstories.json?print=pretty",
		headers={
			"X-Mashape-Key": "dpMuURitoYmsh9R2HxFJf6RDDNd4p1TaF1ljsnEp7IJCIE2E3i",
			"Accept": "application/json"
			}
		)

	latest_id = Article.objects.first().article_id
	print top_articles_id.body[0]
	if latest_id != top_articles_id.body[0]:
		top_articles = []
		for x in top_articles_id.body[0:30]:
			try:
				check_id = Article.objects.get(article_id=x).article_id
				print check_id
			except:
				check_id =None
				pass
			if not check_id:
				article = unirest.get("https://community-hacker-news-v1.p.mashape.com/item/"+str(x)+".json?print=pretty", 
					headers={ 
						"X-Mashape-Key": "dpMuURitoYmsh9R2HxFJf6RDDNd4p1TaF1ljsnEp7IJCIE2E3i",
						"Accept": "application/json"
						}
					)
				top_articles.append(article)
				print "adds"
			else:
				print 'already exists'
		top_articles.reverse()

		for article_object in top_articles:
			title = article_object.body.get('title').encode("utf-8")
			url = article_object.body.get('url')
			author_username = article_object.body.get('by')
			article_id = article_object.body.get('id')
			score = article_object.body.get('score')
			description = 'No descirption yet'

			sentiment_analysis = unirest.get("https://twinword-sentiment-analysis.p.mashape.com/analyze/?text="+title, 
				headers={
					"X-Mashape-Key": "dpMuURitoYmsh9R2HxFJf6RDDNd4p1TaF1ljsnEp7IJCIE2E3i", 
					"Accept": "application/json"
					}
				)

			sentiment_type = sentiment_analysis.body.get('type')
			sentiment_score = abs(int(sentiment_analysis.body.get('score')*100))

			Article.objects.create(
	            title=title,
	            url=url,
	            author_username=author_username,
	            article_id=article_id,
	            score = score,
	            description = description,
	            sentiment_score=sentiment_score,
	            sentiment_type = sentiment_type,
	        )
