from fire import Fire
import time
from ytmusicapi import YTMusic
import time



def main(playlist_name:str='djmax', songtxt:str='song.txt'):
    #login
    try:
        ytmusic = YTMusic('oauth.json')
    except:
        print("you need to run:") 
        print("     $ytmusicapi oauth")
        exit()

    # check if playlist exists: if not, create a new one
    playlists = ytmusic.get_library_playlists()
    playlist_names = [playlist['title'] for playlist in playlists]
    if playlist_name not in playlist_names:
        ytmusic.create_playlist(playlist_name, 'My awesome playlist')


    with open('song.txt', 'r') as f:
        song_names = [line.strip() for line in f]

    # Get the playlist ID for the specified playlist
    playlists = ytmusic.get_library_playlists()
    playlist = next((pl for pl in playlists if pl['title'] == playlist_name), None)
    if playlist is None:
        print(f"Playlist '{playlist_name}' not found!")
        exit()
    playlist_id = playlist['playlistId']

    # Add each song to the playlist
    for song_name in song_names:
        search_results = ytmusic.search(song_name)
        if len(search_results) == 0:
            print(f"No results found for '{song_name}'")
            continue
        song = search_results[0]
        song_id = song['videoId']
        # Add the song to the playlist
        status = ytmusic.add_playlist_items(playlist_id, [song_id])
        if status['status'] != 'STATUS_SUCCEEDED':
            print(f"Failed to add '{song_name}' to playlist!")
            print('usually because you have the song already')
        else:
            print(f"Added '{song_name}' to playlist!")
        time.sleep(.1)

    print("All songs added to playlist!")


if __name__ == '__main__':
    Fire(main)
    '''
    python addsong.py --playlist_name [PL NAME U WANT] --songtxt [TXT that contains song name and artist: used for searching]
    '''
