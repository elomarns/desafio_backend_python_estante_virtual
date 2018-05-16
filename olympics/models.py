from django.db import models
from django.core.validators import MinValueValidator

class Competition(models.Model):
    CRITERIONS_FOR_BEST_RESULT = (
        ("min", "Minimum value"),
        ("max", "Maximum value")
    )

    name = models.CharField(max_length=200, unique=True)
    unit = models.CharField(max_length=10)
    finished = models.BooleanField(default=False)
    results_limit_per_athlete = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    criterion_for_best_result = models.CharField(max_length=3, choices=CRITERIONS_FOR_BEST_RESULT,
        default="max")

    def __str__(self):
        return self.name

    def finish(self):
        self.finished=True
        self.save()
