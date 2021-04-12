from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.IntegerField(null=False)
    projector = models.BooleanField(null=False)


class Booking(models.Model):
    date = models.DateField()
    comment = models.TextField(null=True)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)

    class Meta:
        models.UniqueConstraint(fields=['date', 'room_id'], name='unique_booking')
