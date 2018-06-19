# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Miner(models.Model):
    name = models.CharField(max_length=64)
    ctm = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.name

