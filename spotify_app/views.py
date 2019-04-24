from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.views import View
from .user_data_context import *
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Sum
import requests
import json
from .models import Track, Album, Artist


class Index(View):

    def get(self, request):
        if 'access_token' not in request.session:
            return redirect('callback')

        access_token = request.session.get('access_token')

        authorization_header = {"Authorization": "Bearer {}".format(access_token)}
        try:
            user_profile = get_users_profile(authorization_header)
            tracks = Track.objects.filter(user_id=user_profile['id']).count()
            tracks_oui = Track.objects.filter(user_id=user_profile['id'],like_it='[true]').count()
            tracks_non = Track.objects.filter(user_id=user_profile['id'],like_it='[false]').count()
            albums = Album.objects.filter(user_id=user_profile['id']).count()
            albums_oui = Album.objects.filter(user_id=user_profile['id'],like_it='[true]').count()
            albums_non = Album.objects.filter(user_id=user_profile['id'],like_it='[false]').count()
            artists = Artist.objects.filter(user_id=user_profile['id']).count()
            artists_oui = Artist.objects.filter(user_id=user_profile['id'],like_it='[true]').count()
            artists_non = Artist.objects.filter(user_id=user_profile['id'],like_it='[false]').count()
            tracks_total = Track.objects.all().count()
            tracks_total_oui = Track.objects.filter(like_it='[true]').count()
            tracks_total_non = Track.objects.filter(like_it='[false]').count()
            albums_total = Album.objects.all().count()
            albums_total_oui = Album.objects.filter(like_it='[true]').count()
            albums_total_non = Album.objects.filter(like_it='[false]').count()
            artists_total = Artist.objects.all().count()
            artists_total_oui = Artist.objects.filter(like_it='[true]').count()
            artists_total_non = Artist.objects.filter(like_it='[false]').count()

            ctx = {
                    'user_profile': user_profile,
                    'nb_de_tounne': tracks,
                    'nb_de_album': albums,
                    'tracks_oui': tracks_oui,
                    'tracks_non': tracks_non,
                    'albums_oui': albums_oui,
                    'albums_non': albums_non,
                    'nb_de_artist' : artists,
                    'artists_oui': artists_oui,
                    'artists_non' : artists_non,
                    'tracks_total' : tracks_total,
                    'tracks_total_oui' : tracks_total_oui,
                    'tracks_total_non' : tracks_total_non,
                    'albums_total' : albums_total,
                    'albums_total_oui' : albums_total_oui,
                    'albums_total_non' : albums_total_non,
                    'artists_total' : artists_total,
                    'artists_total_oui' : artists_total_oui,
                    'artists_total_non' : artists_total_non

                    }
            print (ctx)
            return render(request, 'main.html',ctx)
        except KeyError:
            return redirect('callback')    

class Statuser(View):

    def get(self, request):
        if 'access_token' not in request.session:
            return redirect('callback')

        access_token = request.session.get('access_token')

        authorization_header = {"Authorization": "Bearer {}".format(access_token)}
        try:
            user_profile = get_users_profile(authorization_header)
            tracks = Track.objects.filter(user_id=user_profile['id']).count()
            tracks_oui = Track.objects.filter(user_id=user_profile['id'],like_it='[true]').count()
            tracks_non = Track.objects.filter(user_id=user_profile['id'],like_it='[false]').count()
            
            albums = Album.objects.filter(user_id=user_profile['id']).count()
            albums_oui = Album.objects.filter(user_id=user_profile['id'],like_it='[true]').count()
            albums_non = Album.objects.filter(user_id=user_profile['id'],like_it='[false]').count()
            
            dict_track_oui = {'danceability': [], 'speechiness': [], 'acousticness': [],
                              'valence': [], 'instrumentalness': [], 'energy': [], 'liveness': []}
            dict_track_non = {'danceability': [], 'speechiness': [], 'acousticness': [],
                              'valence': [], 'instrumentalness': [], 'energy': [], 'liveness': []}                              
            
            Dancesum = Track.objects.filter(user_id=user_profile['id'],like_it='[true]').aggregate(Sum('danceability'))
            dict_track_oui['danceability'].append(Dancesum['danceability__sum']/tracks_oui)
            Speechsum = Track.objects.filter(user_id=user_profile['id'],like_it='[true]').aggregate(Sum('speechiness'))
            dict_track_oui['speechiness'].append(Speechsum['speechiness__sum']/tracks_oui)
            Acousticsum = Track.objects.filter(user_id=user_profile['id'],like_it='[true]').aggregate(Sum('acousticness'))
            dict_track_oui['acousticness'].append(Acousticsum['acousticness__sum']/tracks_oui)
            Valencesum = Track.objects.filter(user_id=user_profile['id'],like_it='[true]').aggregate(Sum('valence'))
            dict_track_oui['valence'].append(Valencesum['valence__sum']/tracks_oui)
            Instrumentalsum = Track.objects.filter(user_id=user_profile['id'],like_it='[true]').aggregate(Sum('instrumentalness'))
            dict_track_oui['instrumentalness'].append(Instrumentalsum['instrumentalness__sum']/tracks_oui)
            Energysum = Track.objects.filter(user_id=user_profile['id'],like_it='[true]').aggregate(Sum('energy'))
            dict_track_oui['energy'].append(Energysum['energy__sum']/tracks_oui)
            Livenesssum = Track.objects.filter(user_id=user_profile['id'],like_it='[true]').aggregate(Sum('liveness'))
            dict_track_oui['liveness'].append(Livenesssum['liveness__sum']/tracks_oui)
            
            Dancesum = Track.objects.filter(user_id=user_profile['id'],like_it='[false]').aggregate(Sum('danceability'))
            dict_track_non['danceability'].append(Dancesum['danceability__sum']/tracks_non)
            Speechsum = Track.objects.filter(user_id=user_profile['id'],like_it='[false]').aggregate(Sum('speechiness'))
            dict_track_non['speechiness'].append(Speechsum['speechiness__sum']/tracks_non)
            Acousticsum = Track.objects.filter(user_id=user_profile['id'],like_it='[false]').aggregate(Sum('acousticness'))
            dict_track_non['acousticness'].append(Acousticsum['acousticness__sum']/tracks_non)
            Valencesum = Track.objects.filter(user_id=user_profile['id'],like_it='[false]').aggregate(Sum('valence'))
            dict_track_non['valence'].append(Valencesum['valence__sum']/tracks_non)
            Instrumentalsum = Track.objects.filter(user_id=user_profile['id'],like_it='[false]').aggregate(Sum('instrumentalness'))
            dict_track_non['instrumentalness'].append(Instrumentalsum['instrumentalness__sum']/tracks_non)
            Energysum = Track.objects.filter(user_id=user_profile['id'],like_it='[false]').aggregate(Sum('energy'))
            dict_track_non['energy'].append(Energysum['energy__sum']/tracks_non)
            Livenesssum = Track.objects.filter(user_id=user_profile['id'],like_it='[false]').aggregate(Sum('liveness'))
            dict_track_non['liveness'].append(Livenesssum['liveness__sum']/tracks_non)


            table_track_oui = [
                        dict_track_oui['danceability'] ,
                        dict_track_oui['speechiness'] ,
                        dict_track_oui['acousticness'] ,
                        dict_track_oui['valence'] ,
                        dict_track_oui['instrumentalness'] ,
                        dict_track_oui['energy'] ,
                        dict_track_oui['liveness'] 
                             ]
            table_track_non = [
                        dict_track_non['danceability'] ,
                        dict_track_non['speechiness'] ,
                        dict_track_non['acousticness'] ,
                        dict_track_non['valence'] ,
                        dict_track_non['instrumentalness'] ,
                        dict_track_non['energy'] ,
                        dict_track_non['liveness'] 
                             ] 

            dict_track = [tracks_oui, tracks_non]
          
            print(dict_track)


            ctx = {
                    'user_profile': user_profile,
                    'nb_de_tounne': tracks,
                    'nb_de_album': albums,
                    'tracks_oui': tracks_oui,
                    'tracks_non': tracks_non,
                    'albums_oui': albums_oui,
                    'albums_non': albums_non,
                    'table_track_oui' : table_track_oui,
                    'table_track_non' : table_track_non,
                    'dict_track' : dict_track
                    }
            print (ctx)
            return render(request, 'stat_user.html',ctx)
        except KeyError:
            return redirect('callback')


class Kesjecoute(View):

    def get(self, request):
        if 'access_token' not in request.session:
            return redirect('callback')

        access_token = request.session.get('access_token')

        authorization_header = {"Authorization": "Bearer {}".format(access_token)}
        try:
            currently_played = get_users_currently_played(authorization_header)
            currently_played = currently_played['item']    
            tracks4 = get_save_albums(authorization_header, currently_played['album']['id'])
            tracks5 = get_save_track(authorization_header, currently_played['id'])
            tracks6 = get_track(authorization_header, currently_played['id'])
            tracks7 = get_album(authorization_header, currently_played['album']['id'])
            
            
            like = json.dumps(tracks4)
            like_track = json.dumps(tracks5)
            track_isrc = tracks6['external_ids']['isrc']
            album_upc = tracks7['external_ids']['upc']
            artists = currently_played['artists']
            artist_quijoue =  get_artist(authorization_header, artists[0]['id'])

           
           
            ctx = {
                    'currently_played': currently_played,
                    'like': like,
                    'like_track': like_track,
                    'track_isrc': track_isrc,
                    'album_upc': album_upc,
                    'artist': artist_quijoue
                    }
            
         
            return render(request, 'kes_jecoute.html', ctx)
        except:
            return redirect('index')           

class New_Release(View):

    def get(self, request):
        if 'access_token' not in request.session:
            return redirect('callback')

        access_token = request.session.get('access_token')
        authorization_header = {"Authorization": "Bearer {}".format(access_token)}

        new_releases = get_new_releases(authorization_header)
        new_releases = new_releases['albums']['items']

        return render(request, 'new_release.html', {'new_releases': new_releases})

class Callback(View):

    def get(self, request):
        if 'code' in request.GET:

            # pobranie tokena z adresu url
            auth_token = request.GET.get('code')

            code_payload = {
                "grant_type": "authorization_code",
                "code": auth_token,
                "redirect_uri": REDIRECT_URI
            }
            headers = {"Authorization": "Basic {}".format(BASE64)}
            post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)
            response_data = json.loads(post_request.text)

            # zapisanie tokenów do sesji
            request.session['access_token'] = response_data["access_token"]
            request.session['refresh_token'] = response_data["refresh_token"]
            request.session.set_expiry(response_data["expires_in"])

            return redirect('/')
        else:
            return render(request, 'callback.html')


class UserRecentlyPlayedView(View):

    def get(self, request):
        if 'access_token' not in request.session:
            return redirect('callback')
        access_token = request.session.get('access_token')
        authorization_header = {"Authorization": "Bearer {}".format(access_token)}
        recently_played = get_users_recently_played(authorization_header)
        recently_played = recently_played['items']
        
        
        dict_like_track = {'id': [],'track_like': []}
        for track in recently_played:
          
            
            if track['track']['id'] not in recently_played:
                track3 = get_save_track(authorization_header, track['track']['id'])
                like_track = json.dumps(track3)
                dict_like_track['track_like'].append(like_track)

                dict_like_track['id'].append(track['track']['id'])


        print(dict_like_track)
        
        test_list = set(dict_like_track['id'])
        
        print(test_list)
        ctx = {
                    'recently_played': recently_played,
                    'dict_like_track': dict_like_track
                                        
                }
        return render(request,'recently_played.html', ctx)


class AlbumView(View):

    def get(self, request, album_id):
        if 'access_token' not in request.session:
            return redirect('callback')
        access_token = request.session.get('access_token')
        authorization_header = {"Authorization": "Bearer {}".format(access_token)}
        album = get_album(authorization_header, album_id)
        user_profile = get_users_profile(authorization_header)
        tracks = album['tracks']['items']
        popularity = album['popularity']
        artist_id = album['artists'][0]['id']
        dict_isrc_track = {'id': [],'track_isrc': []}
        for track in tracks:
            track = get_track_audio_features(authorization_header, track['id'])
            track2 = get_track(authorization_header, track['id'])
            track_isrc = json.dumps(track2['external_ids']['isrc'])
            dict_isrc_track['track_isrc'].append(track_isrc)
            dict_isrc_track['id'].append(track['id'])
            print(track_isrc)

        tracks4 = get_save_albums(authorization_header, album_id)
        like = json.dumps(tracks4)

        if Album.objects.filter(album_id=album_id,user_id=user_profile['id']).exists():
            spot_album = Album.objects.filter(album_id=album_id,user_id=user_profile['id']).update(like_it=like,popularity = album['popularity'],artist_id = artist_id)
            spot_album = Album.objects.get(album_id=album_id,user_id=user_profile['id'])
        else:
            try:
                tracks_number = len(tracks)
                dict_track = {'danceability': [], 'speechiness': [], 'acousticness': [],
                              'valence': [], 'instrumentalness': [], 'energy': [], 'liveness': [],'track_isrc': []}
                for track in tracks:
                    track = get_track_audio_features(authorization_header, track['id'])
                    
                    dict_track['danceability'].append(float(format(track['danceability'], '.3f')))
                    dict_track['speechiness'].append(float(format(track['speechiness'], '.3f')))
                    dict_track['acousticness'].append(float(format(track['acousticness'], '.3f')))
                    dict_track['valence'].append(float(format(track['valence'], '.3f')))
                    dict_track['instrumentalness'].append(float(format(track['instrumentalness'], '.3f')))
                    dict_track['energy'].append(float(format(track['energy'], '.3f')))
                    dict_track['liveness'].append(float(format(track['liveness'], '.3f')))
                    
                    

                spot_album = Album.objects.create(album_id=album_id, album_artist=album['artists'][0]['name'],artist_id = artist_id,
                                                album_name=album['name'],
                                                upc=album['external_ids']['upc'],
                                                like_it=like,
                                                user_id=user_profile['id'],
                                                user_name=user_profile['display_name'],
                                                danceability=float(format(sum(dict_track['danceability']) / tracks_number, '.3f')),
                                                speechiness=float(format(sum(dict_track['speechiness']) / tracks_number, '.3f')),
                                                acousticness=float(format(sum(dict_track['acousticness']) / tracks_number, '.3f')),
                                                valence=float(format(sum(dict_track['valence']) / tracks_number, '.3f')),
                                                instrumentalness=float(format(sum(dict_track['instrumentalness']) / tracks_number, '.3f')),
                                                energy=float(format(sum(dict_track['energy']) / tracks_number, '.3f')),
                                                liveness=float(format(sum(dict_track['liveness']) / tracks_number, '.3f')),
                                                popularity = album['popularity'])

            except KeyError:
                ctx = {
                    'album': album,
                    'artist_id': artist_id,
                    'upc': album['external_ids']['upc'],
                    'user_name': user_profile['display_name'],
                    'tracks': tracks,
                    'like': like,
                    'dict_isrc_track' : dict_isrc_track,
                    'popularity' : album['popularity']
                    
                }
                return render(request, 'album.html', ctx)
        album_avg = [
            int(spot_album.danceability * 100),
            int(spot_album.speechiness * 100),
            int(spot_album.acousticness * 100),
            int(spot_album.valence * 100),
            int(spot_album.instrumentalness * 100),
            int(spot_album.energy * 100),
            int(spot_album.liveness * 100)]

        ctx = {
            'album': album,
            'upc': album['external_ids']['upc'],
            'user_name': user_profile['display_name'],
            'artist_id': artist_id,
            'tracks': tracks,
            'spot_album': spot_album,
            'album_avg': album_avg,
            'like': like,
            'dict_isrc_track': dict_isrc_track,
            'popularity' : album['popularity']
        }
        return render(request, 'album.html', ctx)


class SpotifyPlaylistsView(View):


    def get(self, request):
        if 'access_token' not in request.session:
            return redirect('callback')
        access_token = request.session.get('access_token')
        authorization_header = {"Authorization": "Bearer {}".format(access_token)}

        # playlist from different decades
        sixties = get_spotify_playlist(authorization_header, '37i9dQZF1DX7Uol5MpckMS')
        seventies = get_spotify_playlist(authorization_header, '37i9dQZF1DX7LGssahBoms')
        eighties = get_spotify_playlist(authorization_header, '37i9dQZF1DWWl7MndYYxge')
        nineties = get_spotify_playlist(authorization_header, '37i9dQZF1DWWGI3DKkKGzJ')
        twentyzero = get_spotify_playlist(authorization_header, '37i9dQZF1DXacPj7eARo6k')
        twentyten = get_spotify_playlist(authorization_header, '37i9dQZF1DX8E06AbSENEw')
        diver1 = get_spotify_playlist(authorization_header, '37i9dQZF1Ejd2YJlaE7jGk')
        diver2 = get_spotify_playlist(authorization_header, '0snqPZNulJzDRfSTeHLykL')
        
        ctx = {
            'sixties': sixties,
            'seventies': seventies,
            'eighties': eighties,
            'nineties': nineties,
            'twentyzero': twentyzero,
            'twentyten': twentyten,
            'diver1': diver1,
            'diver2': diver2

        }
        return render(request, 'spotify_playlists.html', ctx)

class ProjetPlaylistsView(View):


    def get(self, request):
        if 'access_token' not in request.session:
            return redirect('callback')
        access_token = request.session.get('access_token')
        authorization_header = {"Authorization": "Bearer {}".format(access_token)}

        # playlist from different decades
        sixties = get_spotify_playlist(authorization_header, '4nafyLlYBlYdlAfiev1FMi')
        seventies = get_spotify_playlist(authorization_header, '6SDncPPOK5Irhm0frDZ6TO')
        eighties = get_spotify_playlist(authorization_header, '0snqPZNulJzDRfSTeHLykL')
        nineties = get_spotify_playlist(authorization_header, '37i9dQZEVXcSJLvSHFBWrr')
        twentyzero = get_spotify_playlist(authorization_header, '37i9dQZF1Ejd2YJlaE7jGk')
        twentyten = get_spotify_playlist(authorization_header, '37i9dQZF1DWTZeTXqKTge4')
        diver1 = get_spotify_playlist(authorization_header, '37i9dQZF1Ejd2YJlaE7jGk')
        diver2 = get_spotify_playlist(authorization_header, '37i9dQZF1DWTZeTXqKTge4')
        
        ctx = {
            'sixties': sixties,
            'seventies': seventies,
            'eighties': eighties,
            'nineties': nineties,
            'twentyzero': twentyzero,
            'twentyten': twentyten,
            'diver1': diver1,
            'diver2': diver2

        }
        return render(request, 'projet_playlists.html', ctx)

class PlaylistView(View):

    def get(self, request, playlist_id):
        if 'access_token' not in request.session:
            return redirect('callback')
        access_token = request.session.get('access_token')
        authorization_header = {"Authorization": "Bearer {}".format(access_token)}
        playlist_tracks = get_playlist_tracks(authorization_header, playlist_id)
        feature_track = []
        dict_like_track = {'id': [],'track_like': []}
                 
        for track in playlist_tracks['items']:
            feature_track.append(track['track']['id'])
            track3 = get_save_track(authorization_header, track['track']['id'])
            like_track = json.dumps(track3)
            dict_like_track['track_like'].append(like_track)
            dict_like_track['id'].append(track['track']['id'])
        ctx = {
            'playlist_tracks': playlist_tracks,
            'feature_track': feature_track,
            'dict_like_track': dict_like_track
        }
        return render(request, 'playlist.html', ctx)


class TrackAudioFeaturesView(View):

    def get(self, request, track_id):
        if 'access_token' not in request.session:
            return redirect('callback')
        access_token = request.session.get('access_token')
        authorization_header = {"Authorization": "Bearer {}".format(access_token)}
        track = get_track_audio_features(authorization_header, track_id)
        track2 = get_track(authorization_header, track_id)
        track3 = get_save_track(authorization_header, track_id)
        user_profile = get_users_profile(authorization_header)
        like_track = json.dumps(track3)
       
        track_name = track2['name']
        popularity = track2['popularity']
        track_artist = track2['album']['artists'][0]['name']
        artist_id = track2['album']['artists'][0]['id']
        
        if Track.objects.filter(track_id=track_id,user_id=user_profile['id']).exists():
            
                spot_track = Track.objects.filter(track_id=track_id,user_id=user_profile['id']).update(like_it=like_track,popularity = track2['popularity'],artist_id=artist_id)
                spot_track = Track.objects.get(track_id=track_id,user_id=user_profile['id']) 
        else:
            try:
                spot_track = Track.objects.create(track_id=track_id,
                                                track_artist=track_artist,
                                                artist_id=artist_id,
                                                track_name=track_name,
                                                user_id=user_profile['id'],
                                                user_name=user_profile['display_name'],
                                                isrc=track2['external_ids']['isrc'],
                                                mode=float(format(track['mode'], '.3f')),
                                                time_signature=float(format(track['time_signature'], '.3f')),
                                                duration_ms=float(format(track['duration_ms'], '.3f')),
                                                tempo=float(format(track['tempo'], '.3f')),
                                                loudness=float(format(track['loudness'], '.3f')),
                                                danceability=float(format(track['danceability'], '.3f')),
                                                speechiness=float(format(track['speechiness'], '.3f')),
                                                acousticness=float(format(track['acousticness'], '.3f')),
                                                valence=float(format(track['valence'], '.3f')),
                                                instrumentalness=float(format(track['instrumentalness'], '.3f')),
                                                energy=float(format(track['energy'], '.3f')),
                                                liveness=float(format(track['liveness'], '.3f')),
                                                key=track['key'],
                                                like_it=like_track,
                                                popularity = track2['popularity'])
            except KeyError:
                table_track = [
                        int(track['danceability'] * 100),
                        int(track['speechiness'] * 100),
                        int(track['acousticness'] * 100),
                        int(track['valence'] * 100),
                        int(track['instrumentalness'] * 100),
                        int(track['energy'] * 100),
                        int(track['liveness'] * 100)
            
                             ]
                ctx = {
                        'track': track,
                        'user_name': user_profile['display_name'],
                        'spot_track': spot_track,
                        'table_track': table_track,
                        'track_artist': track_artist,
                        'artist_id': artist_id,
                        'track_name': track_name,
                        'isrc' : track2['external_ids']['isrc'],
                        'image_album' : track2['album']['images'],
                        'like_track': like_track,
                        'key': track['key'],
                        'mode':track['mode'],
                        'tempo': float(format(track['tempo'], '.3f')),
                        'popularity': track2['popularity']
                                            }
                print(table_track)                                            
                return render(request, 'track.html', ctx)
        table_track = [
            int(track['danceability'] * 100),
            int(track['speechiness'] * 100),
            int(track['acousticness'] * 100),
            int(track['valence'] * 100),
            int(track['instrumentalness'] * 100),
            int(track['energy'] * 100),
            int(track['liveness'] * 100)
            
            ]
        ctx = {
            'track': track,
            'user_name': user_profile['display_name'],
            'spot_track': spot_track,
            'table_track': table_track,
            'track_artist': track_artist,
            'artist_id': artist_id,
            'track_name': track_name,
            'isrc' : track2['external_ids']['isrc'],
            'image_album' : track2['album']['images'],
            'like_track': like_track,
            'key': track['key'],
            'mode':track['mode'],
            'tempo': float(format(track['tempo'], '.3f')),
            'popularity': track2['popularity']
                   }
        print(table_track)
        return render(request, 'track.html', ctx)


class TracksTableView(View):

    def get(self, request):
        tracks = Track.objects.all()
        return render(request, 'tracks_table.html', {'tracks': tracks})


class SearchView(View):

    def get(self, request):
        if 'access_token' not in request.session:
            return redirect('callback')
        access_token = request.session.get('access_token')
        authorization_header = {"Authorization": "Bearer {}".format(access_token)}
        searching = request.GET.get('q')
        result = search_result(authorization_header, searching)
        result_list = result['artists']
        return render(request, 'search.html', {'result_list': result_list})

class TopArtistsView(View):

    def get(self, request):
        if 'access_token' not in request.session:
            return redirect('callback')
        access_token = request.session.get('access_token')
        authorization_header = {"Authorization": "Bearer {}".format(access_token)}
        result = get_users_top_artist(authorization_header)
       
        return render(request, 'topartists.html', {'result_list': result})        

class PushAlbum(View):

    def put(self, request, album_id):
        if 'access_token' not in request.session:
            return redirect('callback')
        access_token = request.session.get('access_token')
        authorization_header = {"Authorization": "Bearer {}".format(access_token)}

        modelform  = push_save_albums(authorization_header, album_id)
        form = modelform(request.PUT)
        
        return redirect('restview')

class ArtistView(View):

    def get(self, request, artist_id):
        if 'access_token' not in request.session:
            return redirect('callback')
        access_token = request.session.get('access_token')
        authorization_header = {"Authorization": "Bearer {}".format(access_token)}
        user_profile = get_users_profile(authorization_header)
        artist = artist_albums(authorization_header, artist_id)
        artist_all =  get_artist(authorization_header, artist_id)
        artist_name = artist_all['name']
        followers = artist_all['followers']['total']
        popularity = artist_all['popularity']
        genres = artist_all['genres']
        user_id=user_profile['id']
        user_name=user_profile['display_name']
        tracks4 = get_save_artists(authorization_header, artist_id)
        like_it = json.dumps(tracks4)

        if Artist.objects.filter(artist_id=artist_id,user_id=user_profile['id']).exists():
                spot_artist = Artist.objects.filter(artist_id=artist_id,user_id=user_profile['id']).update(like_it=like_it)
                spot_artist = Artist.objects.get(artist_id=artist_id,user_id=user_profile['id']) 
        else:
            try:
                spot_artist = Artist.objects.create(artist_id=artist_id,
                                                artist_name=artist_name,                                                
                                                followers=float(format(followers, '.0f')),
                                                user_id=user_id,
                                                user_name=user_name,
                                                genres = genres,
                                                popularity = popularity,
                                                like_it=like_it)
            except KeyError:
                ctx = {
                        'artist': artist,
                        'spot_artist': spot_artist,
                        'artist_all' : artist_all,
                        'user_name' : user_name,
                        'like_it': like_it
                                            }
                print(artist_all)                                            
                return render(request, 'artist.html', ctx)
        
        ctx = {
                        'artist': artist,
                        'spot_artist': spot_artist,
                        'artist_all' : artist_all,
                        'user_name' : user_name,
                        'like_it': like_it
              }
        print(artist_all)

        return render(request, 'artist.html', ctx)


class AlbumTableView(View):

    def get(self, request):
        albums = Album.objects.all()
        return render(request, 'albums_table.html', {'albums': albums})

class ArtistTableView(View):

    def get(self, request):
        artists = Artist.objects.all()
        return render(request, 'artists_table.html', {'artists': artists})        


