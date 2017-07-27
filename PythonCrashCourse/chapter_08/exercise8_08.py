#!/usr/bin/env python3

def make_album(artist_name, album_title, number_tracks = ''):
    album = {'Artist name': artist_name, 'Album Title': album_title}
    if number_tracks:
        album['Number of tracks'] = number_tracks
    return album

while True:
    print("\nПожалуйста введите описание музыкального альбома:")
    print("(Нажмите 'q' в любое время для выхода)")

    artist_name = input("Имя исполнителя: ")
    if artist_name == 'q':
        break

    album_title = input("Название альбома: ")
    if album_title == 'q':
        break

    formatted_album = make_album(artist_name, album_title)
    print(formatted_album)
