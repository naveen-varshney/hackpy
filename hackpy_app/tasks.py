from __future__ import absolute_import, unicode_literals
from celery import task
import urllib
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
import re
from . import models


#for crawling hackernews homepage
def get_comment(post,user):
    print("++++called By celery crawl_task->get_comment+++++")
    request_data = urllib.urlopen("https://news.ycombinator.com/item?id="+post.post_link_id)
    soup     = BeautifulSoup(request_data, 'html.parser')
    all_comment = soup.find_all("div", class_="comment")
    for com in all_comment:
        post.comments.create(comment_text=com.text,user=user)

@task()
def crawl_task():
    print("++++called By celery crawl_task+++++")
    request_data = urllib.urlopen("https://news.ycombinator.com/")
    soup     = BeautifulSoup(request_data, 'html.parser')
    all_post = soup.find_all("a", class_="storylink")
    all_id   = soup.find_all("span", class_="age")
    all_host = soup.find_all("span", class_="sitestr")
    user     = User.objects.get(id="1")
    for post,post_id,host in zip(all_post,all_id,all_host):
        extract_id = re.findall('\d+', post_id.next_element.get('href'))[0]
        extract_host = host.text
        if models.UserPost.objects.filter(post_link_id=extract_id).first() is None:
            post = models.UserPost.objects.create(user_id=user.id,post_link=post.get('href'),post_title=post.text,post_link_id=extract_id,post_host=extract_host)
            get_comment(post,user)
