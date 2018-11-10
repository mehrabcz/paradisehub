# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class Signup(models.Model):
    phonenumber = models.CharField(max_length=11)
    security_code = models.IntegerField()

    def __str__(self):
        return "%s__%s"%(self.phonenumber, self.security_code)


class apartment(models.Model):
    user = models.OneToOneField(to=User)
    el_area = models.IntegerField()
    count_family = models.IntegerField()


class apartments(models.Model):
    admin_apartment = models.ForeignKey(to=apartment)
    # count_apartment = models.IntegerField()


class Member(models.Model):
    apartment_group = models.ForeignKey(to=apartments)
    member = models.ForeignKey(to=apartment)
