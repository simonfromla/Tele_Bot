from django.conf.urls import url
from .views import CommandReceiveView

urlpatterns = [
    url(r'^26b25cd7590de9af99028e37a8e1aec624c17d8ce2565c2d42/?$',
        CommandReceiveView.as_view())
]
