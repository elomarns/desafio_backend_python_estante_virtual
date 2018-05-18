from contextlib import contextmanager
from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Competition, Athlete, Result

class ValidationErrorTestMixin(object):
    @contextmanager
    def assertValidationErrors(self, fields):
        """
        Assert that a validation error is raised, containing all the specified
        fields, and only the specified fields.
        """
        try:
            yield
            raise AssertionError("ValidationError not raised")
        except ValidationError as e:
            self.assertEqual(set(fields), set(e.message_dict.keys()))


class CompetitionTestCase(ValidationErrorTestMixin, TestCase):
    def test_competition_is_valid_with_required_and_default_fields(self):
        competition = Competition(name="Salto Naquela Plataforma Lá", unit="m")

        try:
            competition.full_clean()
        except ValidationError:
            self.fail("full_clean() raised ValidationError unexpectedly on Competition model")

    def test_competition_is_not_finished_by_default(self):
        competition = Competition()
        self.assertEqual(competition.finished, False)

    def test_competition_has_one_result_per_athlete_by_default(self):
        competition = Competition()
        self.assertEqual(competition.results_limit_per_athlete, 1)

    def test_competition_has_maximum_value_as_the_criterion_for_best_result_by_default(self):
        competition = Competition()
        self.assertEqual(competition.criterion_for_best_result, "max")

    def test_competition_requires_a_name(self):
        competition = Competition(name=None, unit="s")

        with self.assertValidationErrors(["name"]):
            competition.full_clean()

    def test_competition_requires_an_unique_name(self):
        competition = Competition.objects.create(name="Fortnite BR", unit="kills")
        duplicate_competition = Competition(name="Fortnite BR", unit="kills")

        with self.assertValidationErrors(["name"]):
            duplicate_competition.full_clean()

    def test_competition_requires_an_unit(self):
        competition = Competition(name="Degustação de Cachorros-quentes", unit=None)

        with self.assertValidationErrors(["unit"]):
            competition.full_clean()

    def test_competition_requires_a_results_limit_per_athlete(self):
        competition = Competition(name="Xadrez 3D", unit="vitórias", results_limit_per_athlete=None)

        with self.assertValidationErrors(["results_limit_per_athlete"]):
            competition.full_clean()

    def test_competition_requires_a_criterion_for_best_result(self):
        competition = Competition(name="Rocket League", unit="gols", criterion_for_best_result=None)

        with self.assertValidationErrors(["criterion_for_best_result"]):
            competition.full_clean()

    def test_competitions_can_finish_themselves(self):
        competition = Competition()
        competition.finish()
        self.assertEqual(competition.finished, True)


class AthleteTestCase(ValidationErrorTestMixin, TestCase):
    def test_athlete_is_valid_with_name(self):
        athlete = Athlete(name="Elomar Nascimento dos Santos")

        try:
            athlete.full_clean()
        except ValidationError:
            self.fail("full_clean() raised ValidationError unexpectedly on Athlete model")

    def test_athlete_requires_a_name(self):
        athlete = Athlete(name=None)

        with self.assertValidationErrors(['name']):
            athlete.full_clean()

    def test_athlete_requires_an_unique_name(self):
        athlete = Athlete.objects.create(name="Renato Laranja")
        duplicate_athlete = Athlete(name=athlete.name)

        with self.assertValidationErrors(['name']):
            duplicate_athlete.full_clean()

    def test_athlete_string_representation(self):
        athlete = Athlete(name="Napoleon Dynamite")
        self.assertEqual(str(athlete), athlete.name)


class ResultTestCase(ValidationErrorTestMixin, TestCase):
    def setUp(self):
        Competition.objects.create(name="Salto em Distância", unit="m")
        Athlete.objects.create(name="The Undertaker")

    def test_result_is_valid_with_competition_athlete_and_value(self):
        result = Result(competition=Competition.objects.first(),
                        athlete=Athlete.objects.first(),
                        value=7.1)

        try:
            result.full_clean()
        except ValidationError:
            self.fail("full_clean() raised ValidationError unexpectedly on Result model")

    def test_result_requires_a_competition(self):
        result = Result(competition=None,
                        athlete=Athlete.objects.first(),
                        value=5.3)

        with self.assertValidationErrors(["competition"]):
            result.full_clean()

    def test_result_requires_an_athlete(self):
        result = Result(competition=Competition.objects.first(),
                        athlete=None,
                        value=4.2)

        with self.assertValidationErrors(["athlete"]):
            result.full_clean()

    def test_result_requires_a_value(self):
        result = Result(competition=Competition.objects.first(),
                        athlete=Athlete.objects.first(),
                        value=None)

        with self.assertValidationErrors(["value"]):
            result.full_clean()

    def test_result_must_belong_to_a_competition_which_is_not_finished(self):
        competition = Competition.objects.first()
        competition.finished = True

        result = Result(competition=competition,
                        athlete=Athlete.objects.first(),
                        value=8)
        with self.assertValidationErrors(["competition"]):
            result.full_clean()


    def test_result_must_belong_to_an_athlete_who_has_not_reached_his_limit_yet(self):
        result = Result.objects.create(competition=Competition.objects.first(),
                                       athlete=Athlete.objects.first(),
                                       value=5.6)
        result_from_same_athlete = Result(competition=Competition.objects.first(),
                                          athlete=Athlete.objects.first(),
                                          value=6.3)

        with self.assertValidationErrors(["athlete"]):
            result_from_same_athlete.full_clean()
