import uuid
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="login_histories")
    connection_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.login_time} ({self.connection_id})"
