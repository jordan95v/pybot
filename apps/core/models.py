from django.db import models
from config.app_settings import MAX_TIMESTAMP_BETWEEN_PARTICIPATIONS

__all__: list[str] = ["Server", "Student"]


class Server(models.Model):
    discord_id = models.BigIntegerField(unique=True, null=False)
    is_open = models.BooleanField(default=False)
    points_to_give = models.FloatField(default=0.5)


class Student(models.Model):
    class Meta:
        unique_together = ("discord_id", "server")

    discord_id = models.BigIntegerField(null=False)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    class_name = models.CharField(max_length=10, null=False)
    points = models.FloatField(default=0.0)
    last_participation = models.DateTimeField(null=True)
    server = models.ForeignKey(
        Server, on_delete=models.CASCADE, related_name="students"
    )

    def can_participate(self, timestamp: float) -> bool:
        if self.last_participation is None:
            return True
        last_participation: float = self.last_participation.timestamp()
        return timestamp - last_participation >= MAX_TIMESTAMP_BETWEEN_PARTICIPATIONS
