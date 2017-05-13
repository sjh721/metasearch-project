from __future__ import unicode_literals

from django.db import models

class ImageLink(models.Model):
    ImageLink_img = models.CharField(max_length=500)
    ImageLink_link = models.CharField(max_length=500)
    def __str__(self):
        return self.word_text
