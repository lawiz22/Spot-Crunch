"""spotify_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from spotify_app.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', Index.as_view(), name='index'),
    url(r'^kes_jecoute$', Kesjecoute.as_view(), name='kes_jecoute'),
    url(r'^new_release/$', New_Release.as_view(), name='new_release'),
    url(r'^callback/q', Callback.as_view(), name='callback'),
    url(r'^recently_played/$', UserRecentlyPlayedView.as_view(), name='recently_played'),
    url(r'^album/(?P<album_id>[a-zA-Z0-9]+)', AlbumView.as_view(), name='album'),
    url(r'^spotify_playlists/$', SpotifyPlaylistsView.as_view(), name='spotify_playlists'),
    url(r'^projet_playlists/$', ProjetPlaylistsView.as_view(), name='projet_playlists'),
    url(r'^playlist/(?P<playlist_id>[a-zA-Z0-9]+)/', PlaylistView.as_view(), name='playlist'),
    url(r'^track/(?P<track_id>[a-zA-Z0-9]+)', TrackAudioFeaturesView.as_view(), name='track'),
    url(r'tracks_table', TracksTableView.as_view(), name='tracks_table'),
    url(r'albums_table', AlbumTableView.as_view(), name='albums_table'),
    url(r'^https://open.spotify.com/album/(?P<album_id>[a-zA-Z0-9]+)', PushAlbum.as_view(), name='push_album'),
    url(r'search', SearchView.as_view(), name='search'),
    url(r'topartists', TopArtistsView.as_view(), name='topartists'),
    url(r'^artist/(?P<artist_id>.*)/$', ArtistView.as_view(), name='artist')
]
