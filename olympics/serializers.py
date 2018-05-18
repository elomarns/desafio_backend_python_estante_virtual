from rest_framework import serializers
from .models import Competition, Athlete, Result

class AthleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Athlete
        fields = '__all__'


class SimpleResultSerializer(serializers.ModelSerializer):
    athlete = AthleteSerializer(read_only=True)

    class Meta:
        model = Result
        fields = ('id', 'athlete', 'value')


class CompetitionSerializer(serializers.ModelSerializer):
    ranking = SimpleResultSerializer(read_only=True, many=True)
    winner_result = SimpleResultSerializer(read_only=True)

    class Meta:
        model = Competition
        fields = '__all__'


class SimpleCompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = ('id', 'name', 'unit', 'finished', 'results_limit_per_athlete', 'criterion_for_best_result')


class ResultSerializer(serializers.ModelSerializer):
    competition_id = serializers.IntegerField(write_only=True)
    competition = SimpleCompetitionSerializer(read_only=True)
    athlete_id = serializers.IntegerField(write_only=True)
    athlete = AthleteSerializer(read_only=True)

    class Meta:
        model = Result
        fields = '__all__'
