# 🎵 Music Recommender Simulation

## Project Summary

**VibeMatch 1.0** is a small, content-based music recommender written in Python. It loads 18 songs from `data/songs.csv`, compares each song to a listener's taste profile (favorite genre, favorite mood, and target energy), and gives every song a score out of 4: +2 for a genre match, +1 for a mood match, and up to +1 for how close the song's energy is to what the listener wants. It then ranks the songs and prints the top 5, with the reasons each song earned its points. I tested it with six different listener profiles, ran a weight-shift experiment, and documented its strengths, biases, and limitations in the [Model Card](model_card.md).

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

## Stress Test: Different User Profiles

I ran `python -m src.main` with six listener profiles: three normal tastes and two edge cases designed to try to trick the scoring (plus the default). Top 5 for each:

### Default Pop

```
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

### High-Energy Pop

```
============================================================
User profile: genre=pop, mood=happy, energy=0.85
============================================================
1. Sunrise City by Neon Echo  (pop, happy)
   Score: 3.97 / 4.00
   - genre match: pop (+2.0)
   - mood match: happy (+1.0)
   - energy 0.82 vs target 0.85 (+0.97)

2. Gym Hero by Max Pulse  (pop, intense)
   Score: 2.92 / 4.00
   - genre match: pop (+2.0)
   - energy 0.93 vs target 0.85 (+0.92)

3. Rooftop Lights by Indigo Parade  (indie pop, happy)
   Score: 1.91 / 4.00
   - mood match: happy (+1.0)
   - energy 0.76 vs target 0.85 (+0.91)

4. Block Party Anthem by Kid Kairo  (hip-hop, energetic)
   Score: 1.00 / 4.00
   - energy 0.85 vs target 0.85 (+1.00)

5. Storm Runner by Voltline  (rock, intense)
   Score: 0.94 / 4.00
   - energy 0.91 vs target 0.85 (+0.94)
```

### Chill Lofi

```
============================================================
User profile: genre=lofi, mood=chill, energy=0.35
============================================================
1. Library Rain by Paper Lanterns  (lofi, chill)
   Score: 4.00 / 4.00
   - genre match: lofi (+2.0)
   - mood match: chill (+1.0)
   - energy 0.35 vs target 0.35 (+1.00)

2. Midnight Coding by LoRoom  (lofi, chill)
   Score: 3.93 / 4.00
   - genre match: lofi (+2.0)
   - mood match: chill (+1.0)
   - energy 0.42 vs target 0.35 (+0.93)

3. Focus Flow by LoRoom  (lofi, focused)
   Score: 2.95 / 4.00
   - genre match: lofi (+2.0)
   - energy 0.40 vs target 0.35 (+0.95)

4. Spacewalk Thoughts by Orbit Bloom  (ambient, chill)
   Score: 1.93 / 4.00
   - mood match: chill (+1.0)
   - energy 0.28 vs target 0.35 (+0.93)

5. Coffee Shop Stories by Slow Stereo  (jazz, relaxed)
   Score: 0.98 / 4.00
   - energy 0.37 vs target 0.35 (+0.98)
```

### Deep Intense Rock

```
============================================================
User profile: genre=rock, mood=intense, energy=0.9
============================================================
1. Storm Runner by Voltline  (rock, intense)
   Score: 3.99 / 4.00
   - genre match: rock (+2.0)
   - mood match: intense (+1.0)
   - energy 0.91 vs target 0.90 (+0.99)

2. Gym Hero by Max Pulse  (pop, intense)
   Score: 1.97 / 4.00
   - mood match: intense (+1.0)
   - energy 0.93 vs target 0.90 (+0.97)

3. Neon Pulse by DJ Lumen  (edm, euphoric)
   Score: 0.95 / 4.00
   - energy 0.95 vs target 0.90 (+0.95)

4. Block Party Anthem by Kid Kairo  (hip-hop, energetic)
   Score: 0.95 / 4.00
   - energy 0.85 vs target 0.90 (+0.95)

5. Iron Furnace by Grave Signal  (metal, angry)
   Score: 0.93 / 4.00
   - energy 0.97 vs target 0.90 (+0.93)
```

### Sad but High-Energy (edge case)

```
============================================================
User profile: genre=folk, mood=sad, energy=0.9
============================================================
1. Rainy Window by Mara Lune  (folk, sad)
   Score: 3.40 / 4.00
   - genre match: folk (+2.0)
   - mood match: sad (+1.0)
   - energy 0.30 vs target 0.90 (+0.40)

2. Storm Runner by Voltline  (rock, intense)
   Score: 0.99 / 4.00
   - energy 0.91 vs target 0.90 (+0.99)

3. Gym Hero by Max Pulse  (pop, intense)
   Score: 0.97 / 4.00
   - energy 0.93 vs target 0.90 (+0.97)

4. Neon Pulse by DJ Lumen  (edm, euphoric)
   Score: 0.95 / 4.00
   - energy 0.95 vs target 0.90 (+0.95)

5. Block Party Anthem by Kid Kairo  (hip-hop, energetic)
   Score: 0.95 / 4.00
   - energy 0.85 vs target 0.90 (+0.95)
```

### Unknown Genre (edge case)

```
============================================================
User profile: genre=k-pop, mood=happy, energy=0.7
============================================================
1. Rooftop Lights by Indigo Parade  (indie pop, happy)
   Score: 1.94 / 4.00
   - mood match: happy (+1.0)
   - energy 0.76 vs target 0.70 (+0.94)

2. Sunrise City by Neon Echo  (pop, happy)
   Score: 1.88 / 4.00
   - mood match: happy (+1.0)
   - energy 0.82 vs target 0.70 (+0.88)

3. Night Drive Loop by Neon Echo  (synthwave, moody)
   Score: 0.95 / 4.00
   - energy 0.75 vs target 0.70 (+0.95)

4. Dusty Back Roads by The Willow Creek Band  (country, nostalgic)
   Score: 0.85 / 4.00
   - energy 0.55 vs target 0.70 (+0.85)

5. Block Party Anthem by Kid Kairo  (hip-hop, energetic)
   Score: 0.85 / 4.00
   - energy 0.85 vs target 0.70 (+0.85)
```

---

## Experiments You Tried

**Experiment: Weight Shift (half genre, double energy).** I changed the weights from genre 2.0 / mood 1.0 / energy up to 1.0 to **genre 1.0 / mood 1.0 / energy up to 2.0** (the maximum score stays 4.0) and re-ran all six profiles. The weights are named constants at the top of `src/recommender.py` (`GENRE_POINTS`, `MOOD_POINTS`, `ENERGY_POINTS`), so the change only touched those numbers.

| Profile | Before (genre 2 / mood 1 / energy 1) | After (genre 1 / mood 1 / energy 2) |
|---|---|---|
| Default Pop | Sunrise City 3.98, **Gym Hero 2.87**, Rooftop Lights 1.96 | Sunrise City 3.96, **Rooftop Lights 2.92**, Gym Hero 2.74 |
| Chill Lofi | Library Rain 4.00, Midnight Coding 3.93, Focus Flow 2.95 | Library Rain 4.00, Midnight Coding 3.86, Focus Flow 2.90 |
| Deep Intense Rock | Storm Runner 3.99, Gym Hero 1.97, ... Iron Furnace 0.93 (#5) | Storm Runner 3.98, Gym Hero 2.94, ... Iron Furnace 1.86 (#5) |
| Sad but High-Energy | Rainy Window **3.40**, Storm Runner 0.99 | Rainy Window **2.80**, Storm Runner 1.98 |
| Unknown Genre (k-pop) | Rooftop Lights 1.94, Sunrise City 1.88 | Rooftop Lights 2.88, Sunrise City 2.76 |

**What changed:**
- For the default pop/happy user, **Rooftop Lights** (indie pop, happy) moved above **Gym Hero** (pop, intense). That feels *more accurate*: a "happy" listener probably prefers a happy song over an intense gym song, even if the genre label is slightly different.
- For the "sad but high-energy" edge case, the calm folk song **Rainy Window still wins**, but the gap shrank from 2.4 points to 0.8 points. Energy now matters more, but genre + mood (2 points together) still outweigh it.
- Most top-1 picks did not change (Sunrise City, Library Rain, Storm Runner). The experiment mostly **reshuffled positions 2–5** rather than changing who wins.

**Conclusion:** the shift made results a little more accurate for mood-focused listeners, but mostly *different* rather than clearly better. I kept the original weights (genre 2.0) as the default because genre is still the strongest sign of taste for most users, and documented this experiment as evidence of how sensitive the rankings are to the weights.

---

## Limitations and Risks

- **Exact genre matching.** "metal" does not count as "rock" and "indie pop" does not count as "pop," so listeners miss closely related songs. The rock listener got the metal song Iron Furnace only at #5.
- **Genre and mood outweigh energy.** Together they are worth 3 of the 4 points, so a listener who wants sad but high-energy music still gets a calm sad song at #1.
- **Tiny, uneven catalog.** Only 18 made-up songs, and most genres have just one song. Fans of rare genres (or genres not in the catalog, like k-pop) get weaker recommendations.
- **Few features, no behavior data.** It ignores tempo, valence, danceability, acousticness, lyrics, and language, and it has no listening history, so it cannot learn what people actually play or skip.
- **Same songs repeat.** High-energy songs like Block Party Anthem show up in five of the six test listeners' top 5.

More detail is in the Limitations and Bias section of the [Model Card](model_card.md).

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

**How recommenders turn data into predictions.** I learned that a recommender does not "know" what I like. It turns songs into features (genre, mood, energy), turns me into a profile, and then uses a scoring rule to judge every song for that one person and a ranking rule to sort them. The same song gets a different score for different people, which is why the lofi listener and the rock listener got completely different lists. Even with just three features and simple addition, the results felt like real recommendations.

**Where bias and unfairness show up.** I also learned that small design choices create unfairness. Matching genres by exact words hid a metal song from a rock fan, giving genre the most points let it overpower what a listener said about energy, and having more pop and lofi songs in the catalog gives those listeners better results than fans of rare genres. Real apps make these same kinds of choices at a much bigger scale, so the people who design them decide a lot about what music listeners ever get to hear.



