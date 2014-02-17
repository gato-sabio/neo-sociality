from celery import task


@task()
def queue_update(group, days_back):
    from neo_facebook.views import load_newsmaker_posts_into_db
    load_newsmaker_posts_into_db(group, days_back)
    return '[Q] Queue task complete'
