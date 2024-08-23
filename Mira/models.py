from django.db import models

# Create your models here.
class UserLogin(models.Model):
    user_email = models.EmailField(unique=True)  # Ensure unique emails for each user
    user_status = models.BooleanField(default=False)
    user_request = models.IntegerField()

    def __str__(self):
        return self.user_email
