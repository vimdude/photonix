
from django.db import transaction
from django.utils import timezone
from photonix.photos.models import Task

CLASSIFIERS = [
    'color',
    'location',
    'object',
    'style',
]


def process_classify_images_tasks():
    for task in Task.objects.filter(type='classify_images', status='P').order_by('created_at'):
        photo_id = task.subject_id
        generate_classifier_tasks_for_photo(photo_id, task)


def generate_classifier_tasks_for_photo(photo_id, task):
    task.start()
    started = timezone.now()

    # Add task for each classifier on current photo
    with transaction.atomic():
        for classifier in CLASSIFIERS:
            Task(type='classify.{}'.format(classifier), subject_id=photo_id, parent=task).save()
        task.complete_with_children = True
        task.save()