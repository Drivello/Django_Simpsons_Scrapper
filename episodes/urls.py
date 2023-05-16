from django.urls import include,path
from .viewsets import EpisodeViewset#,RandomEpisodeViewset
from rest_framework import routers 

router = routers.DefaultRouter()
router.register(r'episodes', EpisodeViewset)

urlpatterns = router.urls