from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Competition
from .serializers import CompetitionSerializer

class CompetitionViewSet(viewsets.ModelViewSet):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer

    @action(methods=['put', 'patch'], detail=True)
    def finish(self, request, *args, **kwargs):
        competition = self.get_object()
        competition.finish()
        serialized_competition = CompetitionSerializer(competition).data
        return Response(serialized_competition)
