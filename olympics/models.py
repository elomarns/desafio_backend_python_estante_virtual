from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

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


class Athlete(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Result(models.Model):
    competition = models.ForeignKey(Competition, related_name="results", on_delete=models.CASCADE)
    athlete = models.ForeignKey(Athlete, related_name="results", on_delete=models.CASCADE)
    value = models.FloatField()

    def clean(self):
      self.__validate_competition_is_not_finished()
      self.__validate_athlete_is_inside_the_limit_for_competition()

    def __validate_competition_is_not_finished(self):
        if self.competition_id is not None:
            if self.competition.finished:
                raise ValidationError({'competition': "A result can't belong to a finished competition."})

    def __validate_athlete_is_inside_the_limit_for_competition(self):
        if self.competition_id is not None and self.athlete_id is not None:
            amount_of_results = self.competition.results.filter(athlete_id=self.athlete_id).count()
            results_limit = self.competition.results_limit_per_athlete

            if amount_of_results >= results_limit:
                raise ValidationError({'athlete': "This athlete has already reached the limit of results on this competition"})
