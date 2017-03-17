from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from db.models import Bait, Vector, PreyLibrary

class Submitter(models.Model):
    USER_CAT = (
        ('O', 'Omniscient Being'),
        ('R', 'Researcher'),
        ('S', 'Class Student'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    university = models.CharField(max_length=100, null=False)
    department = models.CharField(max_length=100, null=False)
    project_name = models.CharField(max_length=100, null=False, default="rasbase")
    group = models.CharField(max_length=1, choices=USER_CAT, default='R')
    allowed_baits = models.ManyToManyField(Bait)
    allowed_vectors = models.ManyToManyField(Vector)
    prey_library = models.ForeignKey(PreyLibrary, null=True)
    image = models.ImageField(upload_to='profile_images/', default='profile_images/default.jpg')

    def is_omniscient(self):
        if self.group == 'O':
            return True
        else:
            return False

    def get_allowed_baits(self):
        return self.allowed_baits.all()

    def get_allowed_vectors(self):
        return self.allowed_vectors.all()

    def get_prey_library(self):
        return self.prey_library

    def remove_bait_relation(self, bait_name):
        self.allowed_baits.remove(bait_name)

    def remove_vector_relation(self, vector_name):
        self.allowed_vectors.remove(vector_name)
