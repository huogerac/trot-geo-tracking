from django.db import models


class Track(models.Model):
    description = models.CharField(max_length=512)
    circuit = models.ForeignKey("Circuit", models.SET_NULL, blank=True, null=True)
    started = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    def to_dict_json(self):
        return {
            "id": self.id,
            "description": self.description,
            "circuit": self.circuit_id,
            "started": self.started,
            "finished": self.finished,
        }


class Circuit(models.Model):
    name = models.CharField(max_length=512)
    start_line = models.JSONField(default=dict)

    def to_dict_json(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class Point(models.Model):
    track = models.ForeignKey(
        Track,
        on_delete=models.CASCADE,
        related_name="points",
    )
    turn = models.IntegerField()
    point_data = models.JSONField(default=dict)
    ignored = models.BooleanField(default=False)
    created_at_local = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def to_dict_json(self):
        return {
            "id": self.id,
            "track_id": self.track_id,
            "turn": self.turn,
            "point_data": self.point_data,
        }
