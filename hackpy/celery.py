from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackpy.settings')

app = Celery('hackpy')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, crawl_task(), name='add every 10')
    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=9, minute=30),
        crawl_task(),
    )
@app.task()
def crawl_task():
    request_data = urllib.urlopen("https://news.ycombinator.com/")
    soup = BeautifulSoup(request_data, 'html.parser')
    all_post = soup.find_all("a", class_="storylink")
    all_id = soup.find_all("span", class_="age")
    all_host = soup.find_all("span", class_="sitestr")
    user = User.objects.get(id="1")
    for post,post_id,host in zip(all_post,all_id,all_host):
        extract_id = re.findall('\d+', post_id.get('href').encode('utf-8'))[0]
        extract_host = host.text.encode('utf-8')
        UserPost.objects.create(user_id=user.id,post_link=post.get('href').encode('utf-8'),post_title=post.text.encode('utf-8'),post_link_id=extract_id,post_host=extract_host)
