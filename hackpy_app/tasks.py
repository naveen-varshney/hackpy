import re
import requests
import urllib
from bs4 import BeautifulSoup
from .models import UserPost
from django.contrib.auth.models import User
from hackpy.celery import app
from celery import task
#@app.task(bind=True)

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, crawl_task(), name='add every 10')
#     # Executes every Monday morning at 7:30 a.m.
#     sender.add_periodic_task(
#         crontab(hour=9, minute=30),
#         crawl_task(),
#     )
@task(bind=True)
def crawl_task():
    request_data = urllib.urlopen("https://news.ycombinator.com/")
    soup = BeautifulSoup(request_data, 'html.parser')
    all_post = soup.find_all("a", class_="storylink")
    all_id = soup.find_all("span", class_="age")
    all_host = soup.find_all("span", class_="sitestr")
    user = User.objects.get(id="1")
    for post,post_id,host in zip(all_post,all_id,all_host):
        extract_id = re.findall('\d+', post_id.next_element.get('href').encode('utf-8'))[0]
        extract_host = host.text.encode('utf-8')
        UserPost.objects.create(user_id=user.id,post_link=post.get('href').encode('utf-8'),post_title=post.text.encode('utf-8'),post_link_id=extract_id,post_host=extract_host)
