from bowlingapp.views import RetrievePlayerView, CreatePlayerRollView
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bowling.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/game/(?P<game>\d+)/player/(?P<pk>\d+)/$', RetrievePlayerView.as_view(), name='player-detail'),
    url(r'^api/game/(?P<game>\d+)/player/(?P<player>\d+)/roll/$', CreatePlayerRollView.as_view(), name='player-detail'),
    url(r'^admin/', include(admin.site.urls)),
)
