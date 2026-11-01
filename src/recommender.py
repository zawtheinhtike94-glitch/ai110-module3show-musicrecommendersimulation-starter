import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import asdict, dataclass

# Columns in songs.csv that hold numbers; everything else stays as text.
INT_COLUMNS = {"id"}
FLOAT_COLUMNS = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}

# Algorithm Recipe weights (see README "Scoring rule").
GENRE_POINTS = 2.0
MOOD_POINTS = 1.0
ENERGY_POINTS = 1.0  # max points for a perfect energy match

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Song objects for this user, highest score first."""
        prefs = _profile_to_prefs(user)
        return sorted(self.songs, key=lambda song: score_song(prefs, asdict(song))[0], reverse=True)[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a readable sentence listing why this song got its score."""
        score, reasons = score_song(_profile_to_prefs(user), asdict(song))
        return f"Score {score:.2f}: " + "; ".join(reasons)


def _profile_to_prefs(user: UserProfile) -> Dict:
    """Convert a UserProfile into the user_prefs dictionary that score_song expects."""
    return {
        "favorite_genre": user.favorite_genre,
        "favorite_mood": user.favorite_mood,
        "target_energy": user.target_energy,
    }

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv into a list of dicts, converting number columns to int/float."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            # csv gives every value as text, so convert number columns for math later.
            for column in INT_COLUMNS:
                row[column] = int(row[column])
            for column in FLOAT_COLUMNS:
                row[column] = float(row[column])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against the user's prefs; return (score, list of reasons)."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs["favorite_genre"]:
        score += GENRE_POINTS
        reasons.append(f"genre match: {song['genre']} (+{GENRE_POINTS:.1f})")

    if song["mood"] == user_prefs["favorite_mood"]:
        score += MOOD_POINTS
        reasons.append(f"mood match: {song['mood']} (+{MOOD_POINTS:.1f})")

    # Closer energy earns more points: identical energy = full ENERGY_POINTS, opposite ends = 0.
    energy_points = ENERGY_POINTS * (1.0 - abs(song["energy"] - user_prefs["target_energy"]))
    score += energy_points
    reasons.append(
        f"energy {song['energy']:.2f} vs target {user_prefs['target_energy']:.2f} (+{energy_points:.2f})"
    )

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort highest first, and return the top k as (song, score, explanation)."""
    # Judge every song, then rank: sorted() returns a new list, highest score first.
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))

    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    return ranked[:k]
