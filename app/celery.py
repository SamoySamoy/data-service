from celery import Celery

# Create the Celery app
celery_app = Celery('app')

# Configure Celery
celery_app.conf.broker_url = 'redis://localhost:6379/0'
celery_app.conf.result_backend = 'redis://localhost:6379/0'

celery_app.autodiscover_tasks(['app.crawl'])