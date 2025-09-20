from django.template.defaultfilters import truncatechars
from django.db import models

class TrackingModel(models.Model):
    '''
        Helper to make sure that every time we create
        a model we can quickly add the "created_at" and
        "updated_at" details at once.
    '''
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Label this model because we shouldn't use this
        # model to create new instances
        abstract = True
        # Descending order of field  "created_at"
        ordering = ('-created_at',)


class BasicModel(models.Model):
    name = models.CharField(max_length=150, verbose_name="Name", blank=True, null=True, unique=True)
    description = models.TextField(verbose_name="Description", blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)

    @property
    def short_description(self):
        return truncatechars(self.description, 50)