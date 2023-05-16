from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Episode
from .serializers import EpisodeSerializer
import random

class EpisodeViewset(viewsets.ModelViewSet):
    serializer_class = EpisodeSerializer
    queryset = Episode.objects.all()

    def get_season_list(self):
        seasons = self.request.query_params.get('seasons')
        if seasons:
            if seasons[0] + seasons[-1] == '[]':
                seasons = seasons[1:-1]
            seasons_list = seasons.split(',')
            return seasons_list
        else:
            return None

    def get_queryset(self):
        queryset = super().get_queryset()
        seasons_list = self.get_season_list()
        if seasons_list is not None:
            queryset = queryset.filter(season_number__in=seasons_list)
        return queryset
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        
        try:
            instance = Episode.objects.get(number=validated_data['number'], season_number=validated_data['season_number'])
        except Episode.DoesNotExist:
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(instance)
        serializer.instance = instance
        self.perform_update(serializer)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['GET'])
    def random(self,request):
        queryset = super().get_queryset()
        if queryset.exists():
            seasons_list = self.get_season_list()
            if seasons_list is None:
                random_episode = random.choice(queryset)
                serializer = EpisodeSerializer(random_episode)
                return Response(serializer.data)
            else:
                queryset = queryset.filter(season_number__in=seasons_list)
                if queryset.exists():
                    print('season exists')
                    random_episode = random.choice(queryset)
                    serializer = EpisodeSerializer(random_episode)
                    return Response(serializer.data)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    