import re

def clean_trackTitle(trackTitle):
    trackTitle_clean = re.sub(r"\(\s*(from|feat\.?)\b[^)]*\)", "", trackTitle, flags=re.IGNORECASE)
    trackTitle_clean = re.sub(r"/.*$", "", trackTitle_clean)
    trackTitle_clean = re.sub(r"\s{2,}", " ", trackTitle_clean).strip()

    return trackTitle_clean

def get_primary_artist(artists):
    all_artists = re.split(r'\sand\s|\sfeaturing\s|\sfeat\.\s|\swith\s|,\s', artists, flags=re.IGNORECASE)
    primary_artist = all_artists[0].strip()

    return primary_artist

def get_decade(date):
    year = date.year
    decade = (year // 10) * 10

    return decade

def get_popular_songs(full_charts):
    full_charts['trackTitle'] = full_charts['trackTitle'].apply(clean_trackTitle)
    full_charts['primary_artist'] = full_charts['artists'].apply(get_primary_artist)
    full_charts['decade'] = full_charts['date'].apply(get_decade)

    popular_songs = full_charts.drop_duplicates(subset=['trackTitle', 'primary_artist', 'decade'], keep='first')
    popular_songs = popular_songs.sort_values(by='primary_artist').reset_index(drop=True)

    return popular_songs