#!/usr/bin/env python3

def make_album(artist_name, album_title, number_tracks = ''):
    album = {'Artist name': artist_name, 'Album Title': album_title}
    if number_tracks:
        album['Number of tracks'] = number_tracks
    return album

album = make_album('Massive Attack', 'Heligoland', '10')
print(album)
album = make_album('Nirvana', 'Nevermind')
print(album)
album = make_album('Jefferson Airplane', 'Surrealistic Pillow', '11')
print(album)
