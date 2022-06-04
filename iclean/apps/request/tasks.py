from celery import shared_task


# Create your tasks here
@shared_task
def add(x, y):
    return x + y

@shared_task
def mul(x, y):
    return x * y

@shared_task
def say_hello():
    return 'Hello from Celery background task worker!'
