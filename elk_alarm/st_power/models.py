# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class st_power(models.Model):
    miner = models.CharField(max_length=32)
    power = models.IntegerField
    status = models.BooleanField
    user = models.CharField(max_length=32)
    ctm = models.DateTimeField
    utm = models.DateTimeField

    # def __init__(self, arg):
    #     super(Great_power_miner, self).__init__()
    #     self.arg = arg

