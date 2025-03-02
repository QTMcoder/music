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
    Fetches all album information using the Spotify API.
    """
    url = f'https://api.spotify.com/v1/albums/{album_id}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()  # Return the entire album data
    else:
        print(f"Error fetching album {album_id}: {response.status_code} - {response.text}")
        return None

def get_artist_info(artist_id, access_token):
    """
    Fetches all artist information using the Spotify API.
    """
    url = f'https://api.spotify.com/v1/artists/{artist_id}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()  # Return the entire artist data
    else:
        print(f"Error fetching artist {artist_id}: {response.status_code} - {response.text}")
        return None

def save_to_csv(data, filename):
    """
    Saves data to a CSV file with dynamic headers.
    """
    if not data:
        print(f"No data to save for {filename}.")
        return

    # Extract headers dynamically from the first item in the data
    fieldnames = data[0].keys()
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
    save_to_csv(albums_data, 'albums.csv')
    save_to_csv(artists_data, 'artists.csv')
    print("Data saved to albums.csv and artists.csv!")

if __name__ == "__main__":
    main()