from django.db import models
import uuid

# Create your models here.


class Game(models.Model):
    class Status:
        FINISHED = 0
        STARTED = 1
        FAILED = 2

        CHOICES = (

            (STARTED, 'Started'),
            (FINISHED, 'Finished'),
        )

    id = models.UUIDField(verbose_name='Game', default=uuid.uuid4, primary_key=True, editable=False )
    date_start = models.DateTimeField(auto_now_add=True, verbose_name="startGame")
    date_end = models.DateTimeField(verbose_name="endGame", help_text='время окончания игры', null=True)
    status = models.SmallIntegerField(default=Status.STARTED, choices=Status.CHOICES)
    winner = models.CharField(max_length=50, verbose_name="Победитель", null=True)


class User(models.Model):
    status_user = (
        (1, 'ready'),
        (2, 'not_ready'),
    )
    name = models.CharField(max_length=50)
    ship = models.CharField( max_length=1000, null=True)
    status = models.SmallIntegerField(default=2, choices=status_user)
    game = models.ForeignKey(to="Game", verbose_name="UUID", on_delete=models.CASCADE)

