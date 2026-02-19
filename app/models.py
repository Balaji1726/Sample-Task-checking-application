from django.db import models

class USER(models.Model):
    USERNAME = models.CharField(max_length=100)
    PASSWORD = models.CharField(max_length=100)

    def __str__(self):
        return self.USERNAME


class TASK(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
