from rest_framework import serializers
from .models import Competition, Athlete, Result

class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = '__all__'


class AthleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Athlete
        fields = '__all__'


class ResultSerializer(serializers.ModelSerializer):
    competition_id = serializers.IntegerField(write_only=True)
    competition = CompetitionSerializer(read_only=True)
    athlete_id = serializers.IntegerField(write_only=True)
    athlete = AthleteSerializer(read_only=True)

    class Meta:
        model = Result
        fields = '__all__'
