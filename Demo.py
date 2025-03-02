import csv
import requests
from get_access_token import get_access_token

def read_ids_from_txt(file_path):
    """
    Reads album and artist IDs from a text file.
    """
    album_ids = []
    artist_ids = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        current_section = None
        for line in lines:
            line = line.strip()
            if line == 'album_ids:':
                current_section = 'album_ids'
            elif line == 'artist_ids:':
                current_section = 'artist_ids'
            elif line and current_section == 'album_ids':
                album_ids.append(line)
            elif line and current_section == 'artist_ids':
                artist_ids.append(line)
        return album_ids, artist_ids

def get_album_info(album_id, access_token):
    """
    Fetches album information using the Spotify API.
    """
    url = f'https://api.spotify.com/v1/albums/{album_id}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        album_data = response.json()
        return {
            'album_id': album_data['id'],
            'name': album_data['name'],
            'artist_id': album_data['artists'][0]['id'],
            'release_date': album_data['release_date'],
            'total_tracks': album_data['total_tracks']
        }
    else:
        print(f"Error fetching album {album_id}: {response.status_code} - {response.text}")
        return None

def get_artist_info(artist_id, access_token):
    """
    Fetches artist information using the Spotify API.
    """
    url = f'https://api.spotify.com/v1/artists/{artist_id}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        artist_data = response.json()
        return {
            'artist_id': artist_data['id'],
            'name': artist_data['name'],
            'followers': artist_data['followers']['total'],
            'genres': ', '.join(artist_data['genres']),
            'popularity': artist_data['popularity']
        }
    else:
        print(f"Error fetching artist {artist_id}: {response.status_code} - {response.text}")
        return None

def save_to_csv(data, filename, fieldnames):
    """
    Saves data to a CSV file.
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def main():
    # Fetch access token
    access_token = get_access_token()
    if not access_token:
        print("Failed to get access token.")
        return

    # Read album and artist IDs from the text file
    album_ids, artist_ids = read_ids_from_txt('ids.txt')

    # Fetch album and artist data
    albums_data = []
    artists_data = []

    for album_id in album_ids:
        album_info = get_album_info(album_id, access_token)
        if album_info:
            albums_data.append(album_info)

    for artist_id in artist_ids:
        artist_info = get_artist_info(artist_id, access_token)
        if artist_info:
            artists_data.append(artist_info)

    # Save data to CSV files
    save_to_csv(albums_data, 'albums.csv', fieldnames=['album_id', 'name', 'artist_id', 'release_date', 'total_tracks'])
    save_to_csv(artists_data, 'artists.csv', fieldnames=['artist_id', 'name', 'followers', 'genres', 'popularity'])
    print("Data saved to albums.csv and artists.csv!")

if __name__ == "__main__":
    main()