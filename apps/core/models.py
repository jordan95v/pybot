from django.db import models


class Server(models.Model):
    discord_id = models.BigIntegerField(unique=True, null=False)
    is_open = models.BooleanField(default=False)


class Student(models.Model):
    class Meta:
        unique_together = ("discord_id", "server")

    discord_id = models.BigIntegerField(unique=True, null=False)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    class_name = models.CharField(max_length=10, null=False)
    server = models.ForeignKey(
        Server, on_delete=models.CASCADE, related_name="students"
    )
