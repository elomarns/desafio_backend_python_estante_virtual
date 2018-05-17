from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Competition, Athlete, Result
from .serializers import CompetitionSerializer, AthleteSerializer, ResultSerializer

class CompetitionViewSet(viewsets.ModelViewSet):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer

    @action(methods=['put', 'patch'], detail=True)
    def finish(self, request, *args, **kwargs):
        competition = self.get_object()
        competition.finish()
        serialized_competition = CompetitionSerializer(competition).data
        return Response(serialized_competition)


class CreateResult(APIView):
    def post(self, request):
        result_data = {
            "competition_id": self.__get_competition_id(request.data),
            "athlete_id":  self.__get_athlete_id(request.data),
            "value": request.data.get("value")
        }

        result_serializer = ResultSerializer(data=result_data)

        if result_serializer.is_valid():
            result_serializer.save()
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(result_serializer.errors)

    def __get_competition_id(self, request_data):
        if request_data.get("competition_id") is not None:
            return request_data.get("competition_id")
        elif request_data.get("competition") is not None:
            competition_data = {"name": request_data.get("competition"),
                "unit": request_data.get("unit")}
            competition = self.__get_or_create_competition(competition_data)

            if competition is not None:
                return competition.pk

    def __get_or_create_competition(self, competition_data):
        try:
            if competition_data["unit"] is not None:
                competition = Competition.objects.get(name=competition_data["name"],
                    unit=competition_data["unit"])
            else:
                competition = Competition.objects.get(name=competition_data["name"])
        except Competition.DoesNotExist:
            competition_serializer = CompetitionSerializer(data=competition_data)

            if competition_serializer.is_valid():
                competition = competition_serializer.save()
            else:
                competition = None

        return competition

    def __get_athlete_id(self, request_data):
        if request_data.get("athlete_id") is not None:
            return request_data.get("athlete_id")
        elif request_data.get("athlete") is not None:
            athlete_data = {"name": request_data.get("athlete")}
            athlete = self.__get_or_create_athlete(athlete_data)

            if athlete is not None:
                return athlete.pk

    def __get_or_create_athlete(self, athlete_data):
        try:
            athlete = Athlete.objects.get(name=athlete_data["name"])
        except Athlete.DoesNotExist:
            athlete_serializer = AthleteSerializer(data=athlete_data)

            if athlete_serializer.is_valid():
                athlete = athlete_serializer.save()
            else:
                athlete = None

        return athlete


class ResultDetail(generics.RetrieveAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
