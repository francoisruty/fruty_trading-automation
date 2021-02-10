from celery import Celery
import os

app = Celery('celery', broker=os.environ['BROKER'], backend='rpc://', include=['worker.tasks'])

# cf https://github.com/celery/celery/issues/2788
# We want to disable prefetching entirely since we have long running tasks
app.conf.update(
    CELERYD_PREFETCH_MULTIPLIER=1,
    CELERYD_CONCURRENCY=1,
    CELERY_ACKS_LATE=True,
)
