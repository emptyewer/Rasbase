from __future__ import unicode_literals
import time
from django.db import models
from django.contrib.auth.models import User
from db.models import Bait, Vector, IndexedGenome, PreyLibrary


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'pending/{0}/{1}/{2}'.format(instance.upload.user.username,
                                        time.strftime("%Y-%m-%d"),
                                        filename)

# Create your models here.
class Upload(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

class File(models.Model):
    upload = models.ForeignKey(Upload)
    TYPES = (
        ('B', 'Bait'),
        ('V', 'Vector')
    )
    id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to=user_directory_path)
    type = models.CharField(choices=TYPES, max_length=1)
    bait = models.ForeignKey(Bait, null=True)
    vector = models.ForeignKey(Vector, null=True)
    indexed_genome = models.ForeignKey(IndexedGenome)
    prey_library = models.ForeignKey(PreyLibrary)

