"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

# Test listeners for Phase 4: three normal tastes plus two "tricky" edge cases.
PROFILES = {
    "Default Pop": {"favorite_genre": "pop", "favorite_mood": "happy", "target_energy": 0.8},
    "High-Energy Pop": {"favorite_genre": "pop", "favorite_mood": "happy", "target_energy": 0.85},
    "Chill Lofi": {"favorite_genre": "lofi", "favorite_mood": "chill", "target_energy": 0.35},
    "Deep Intense Rock": {"favorite_genre": "rock", "favorite_mood": "intense", "target_energy": 0.9},
    # Edge case: the only sad song (a calm folk track) clashes with wanting very high energy.
    "Sad but High-Energy (edge case)": {"favorite_genre": "folk", "favorite_mood": "sad", "target_energy": 0.9},
    # Edge case: a genre that is not in the catalog at all.
    "Unknown Genre (edge case)": {"favorite_genre": "k-pop", "favorite_mood": "happy", "target_energy": 0.7},
}


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, user_prefs in PROFILES.items():
        print(f"\n### {name}")
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(user_prefs, recommendations)


def print_recommendations(user_prefs: dict, recommendations: list) -> None:
    """Print the profile and a numbered list of songs with their scores and reasons."""
    print("=" * 60)
    print(
        f"User profile: genre={user_prefs['favorite_genre']}, "
        f"mood={user_prefs['favorite_mood']}, energy={user_prefs['target_energy']}"
    )
    print("=" * 60)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} by {song['artist']}  ({song['genre']}, {song['mood']})")
        print(f"   Score: {score:.2f} / 4.00")
        for reason in explanation.split("; "):
            print(f"   - {reason}")
        print()


if __name__ == "__main__":
    main()
