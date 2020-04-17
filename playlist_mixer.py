import sys
import spotipy
import credentials
import spotify_token as generator


def check_args():
    if len(sys.argv) <= 1:
        print("Whoops, need a second username!")
        print("usage: python {0} [username] [playlist_name]".format(sys.argv[0]))
        sys.exit()


def gather_track_ids_from_result(tracks_to_append):
    tracks = []
    for i, item in enumerate(tracks_to_append['items']):
        track = item['track']
        tracks.append(track['id'])
    return tracks


def iterate_playlist_of_user_for_track_ids(playlist, username, spotify):
    track_ids = []
    if playlist['owner']['id'] == username:  # is playlist from user
        results = spotify.playlist(playlist['id'], fields="tracks,next")
        tracks = results['tracks']
        track_ids.extend(gather_track_ids_from_result(tracks))
        while tracks['next']:
            tracks = spotify.next(tracks)
            track_ids.extend(gather_track_ids_from_result(tracks))
    return track_ids


def track_ids_for_user(username, spotify):
    track_ids = []
    playlists = spotify.user_playlists(username)['items']
    for playlist in playlists:
        track_ids.extend(iterate_playlist_of_user_for_track_ids(playlist, username, spotify))
    return track_ids


def main():
    check_args()
    username_a = credentials.USERNAME
    username_b = sys.argv[1]  # from script call
    playlist_name = '{0}_{1}'.format(username_a, username_b)
    if len(sys.argv) > 2:
        playlist_name = sys.argv[2]
    token_read = generator.get_token()
    print('Received Spotify read token')
    sp_read = spotipy.Spotify(auth=token_read)
    print('Authenticated read permissions')

    all_track_ids = track_ids_for_user(username_a, sp_read)
    print('Gathered user {0}s tracks'.format(username_a))
    all_track_ids.extend(track_ids_for_user(username_b, sp_read))
    print('Gathered user {0}s tracks'.format(username_b))

    token_write = generator.get_token('playlist-modify-public')

    sp = spotipy.Spotify(auth=token_write)
    print('Received Spotify write token')
    playlist_id = sp.user_playlist_create(username_a, playlist_name)['id']
    print('Created Spotify playlist with name {0} for user {1}'.format(playlist_name, username_a))
    i = 0
    count = 0
    track_subset = []
    for track_id in all_track_ids:
        track_subset.append(track_id)
        i += 1
        if i == 100:
            sp.user_playlist_add_tracks(username_a, playlist_id, track_subset)
            count += i
            print('Added round {0} of all tracks to playlist {1}'.format(int(count / 100), playlist_name))
            i = 0
            track_subset = []
    if i > 0:
        sp.user_playlist_add_tracks(username_a, playlist_id, track_subset)
        print('Added final {0} tracks to playlist {1}'.format(i, playlist_name))
    print('Done merging all playlist tracks from {0} and {1} into playlist {2} of user {1}, total number of '
          'tracks: {3}'.format(username_b, username_a, playlist_name, count + len(track_subset)))


if __name__ == '__main__':
    main()
