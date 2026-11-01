# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

**How real apps do it.** Apps like Spotify and YouTube use two main ideas. *Collaborative filtering* looks at what other people do: if people with taste like mine liked a song, I will probably like it too. It uses data like likes, skips, replays, and playlists. *Content-based filtering* looks at the song itself: if I like happy, high-energy pop, it finds other songs with a similar genre, mood, and energy. Real apps mix both.

**What my version does.** My simulator is content-based, because my data only has song attributes (no other users). It gives every song a score that shows how well it matches the user's taste, then recommends the songs with the highest scores. It cares most about genre, then mood, then how close the song's energy is to what the user wants.

**Features each `Song` uses:**
- `genre` (for example pop, lofi, rock)
- `mood` (for example happy, chill, intense)
- `energy` (a number from 0 to 1)
- The other columns (`tempo_bpm`, `valence`, `danceability`, `acousticness`) are loaded but not used in my first scoring rule.

**What the `UserProfile` stores:**
- `favorite_genre`
- `favorite_mood`
- `target_energy` (the energy level the user likes, from 0 to 1)
- `likes_acoustic` (stored, but not used in my first scoring rule)

**Scoring rule (one song):**
- Genre matches the user's favorite genre: **+2 points**
- Mood matches the user's favorite mood: **+1 point**
- Energy closeness: **+ (1 − |song energy − target energy|)**, so a song with energy close to what the user wants gets almost 1 point, and a far one gets less
- Best possible score: 2 + 1 + 1 = **4**

I made genre worth more than mood because genre is the strongest sign of taste, while mood changes from day to day.

**Ranking rule (all songs):** score every song in `songs.csv`, sort them from highest to lowest score, and recommend the top *k* songs (for example the top 5).

**Dataset.** I expanded `data/songs.csv` from 10 to 18 songs. The 8 new songs add genres and moods that were missing (hip-hop, classical, country, metal, r&b, edm, reggae, folk; energetic, peaceful, nostalgic, angry, romantic, euphoric, laid-back, sad), with energy from very calm (0.20) to very intense (0.97).

**User profile used for testing:**

```python
user_prefs = {"favorite_genre": "pop", "favorite_mood": "happy", "target_energy": 0.8}
```

**Biases I expect:**
- **Genre is worth the most (2 points),** so the system may over-prioritize genre and rank a pop song with the wrong mood above a non-pop song that matches the user's mood and energy.
- **Exact word matching is narrow.** "indie pop" does not count as "pop", so a pop fan gets 0 genre points for a song they would probably like.
- **Small, uneven catalog.** Most genres have only one song, so users who like rare genres get fewer good matches than pop or lofi fans.
- **Only three features.** Tempo, valence, danceability, and acousticness are ignored, so two songs with the same genre, mood, and energy look identical even if they sound very different.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `python -m src.main` with the default pop / happy / 0.8 profile:

```
Loaded songs: 18
============================================================
User profile: genre=pop, mood=happy, energy=0.8
============================================================
1. Sunrise City by Neon Echo  (pop, happy)
   Score: 3.98 / 4.00
   - genre match: pop (+2.0)
   - mood match: happy (+1.0)
   - energy 0.82 vs target 0.80 (+0.98)

2. Gym Hero by Max Pulse  (pop, intense)
   Score: 2.87 / 4.00
   - genre match: pop (+2.0)
   - energy 0.93 vs target 0.80 (+0.87)

3. Rooftop Lights by Indigo Parade  (indie pop, happy)
   Score: 1.96 / 4.00
   - mood match: happy (+1.0)
   - energy 0.76 vs target 0.80 (+0.96)

4. Block Party Anthem by Kid Kairo  (hip-hop, energetic)
   Score: 0.95 / 4.00
   - energy 0.85 vs target 0.80 (+0.95)

5. Night Drive Loop by Neon Echo  (synthwave, moody)
   Score: 0.95 / 4.00
   - energy 0.75 vs target 0.80 (+0.95)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



