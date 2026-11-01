# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

The recommender works like a judge giving points to every song in the catalog.

- **What it looks at in each song:** the genre (like pop or lofi), the mood (like happy or chill), and the energy level (a number from 0, very calm, to 1, very intense).
- **What it knows about the user:** their favorite genre, their favorite mood, and how energetic they like their music.
- **How it gives points:** if the song's genre is the user's favorite, it gets 2 points. If the mood matches, it gets 1 more point. Then it gets up to 1 extra point for energy: the closer the song's energy is to what the user likes, the more points it gets. A perfect match scores 4.
- **How it picks songs:** it scores all the songs, puts them in order from most to fewest points, and recommends the top 5. For each one, it also lists the reasons it earned its points.
- **Changes from the starter:** the starter code returned no recommendations. I added loading the song file, the point system above, the ranking, and the list of reasons. I made genre worth the most because it is the strongest sign of someone's taste.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

**Main weakness: exact genre matching treats similar genres as completely different.** The system only gives genre points when the song's genre is the exact same word as the user's favorite, so "metal" does not count as "rock" and "indie pop" does not count as "pop." In my tests, the Deep Intense Rock listener got the metal song Iron Furnace only at #5 with 0.93 points, even though a rock fan would probably enjoy it, while the pop song Gym Hero ranked #2 just because its energy was close. This creates a small "filter bubble": users only see songs with their exact genre label and miss closely related music. It also favors users whose favorite genre appears many times in the catalog (pop and lofi) over users of rare genres, and a user whose genre is not in the catalog at all (like k-pop) can never score above 2 out of 4.

**Other limitations I noticed:**
- Genre and mood together (3 points) outweigh energy (1 point), so the "sad but high-energy" listener still got a calm folk song at #1.
- The catalog is small (18 songs) and most genres have only one song.
- Tempo, valence, danceability, and acousticness are ignored, and there is no popularity or listening-history data, so the system cannot learn what people actually play or skip.

---

## 7. Evaluation  

**Profiles I tested.** I ran the recommender for six pretend listeners and looked at each one's top 5 songs (full output is in the README under "Stress Test"):

1. **Default Pop**: pop, happy, energy 0.8
2. **High-Energy Pop**: pop, happy, energy 0.85
3. **Chill Lofi**: lofi, chill, energy 0.35
4. **Deep Intense Rock**: rock, intense, energy 0.9
5. **Sad but High-Energy** (edge case): folk, sad, energy 0.9, a mix that no song in the catalog really fits
6. **Unknown Genre** (edge case): k-pop, happy, energy 0.7, a genre that is not in the catalog

**What I looked for.** Does the #1 song fit the listener's taste? Do the rest of the top 5 "feel" right? Does each listener get a different list, or does the same song keep winning?

**What surprised me.**
- The metal song Iron Furnace was only #5 for the rock fan, because "metal" and "rock" count as totally different genres.
- For the sad but high-energy listener, the calm sad folk song still won by a lot (3.40 vs 0.99). The listener's wish for energy barely mattered.
- The energetic songs Block Party Anthem (in five of the six top-5 lists) and Gym Hero (in four) kept showing up, not because they fit those listeners well but because many listeners wanted high energy.

**Comparing each pair of profiles.**
- **Default Pop vs High-Energy Pop:** almost the same list. Raising energy from 0.8 to 0.85 only swapped the #5 song (Night Drive Loop out, the faster Storm Runner in). This makes sense because the two listeners are nearly identical.
- **Default Pop vs Chill Lofi:** completely different lists with no songs in common. The pop listener gets bright, upbeat songs and the lofi listener gets quiet study music, which is exactly what their genre, mood, and energy ask for.
- **Default Pop vs Deep Intense Rock:** both lists include the gym song Gym Hero, because both listeners want high energy, but the #1 changes from happy pop (Sunrise City) to loud rock (Storm Runner).
- **Default Pop vs Sad but High-Energy:** the pop listener gets happy songs at the top, while the sad listener gets the one sad folk song at #1 followed by loud songs that only match on energy. That shows how mood changes the top pick.
- **Default Pop vs Unknown Genre (k-pop):** the k-pop listener gets the happy pop songs (Rooftop Lights, Sunrise City) because they match "happy," but with much lower scores (under 2), since no song matches k-pop. That is a sensible fallback.
- **High-Energy Pop vs Chill Lofi:** opposite ends of the energy scale, so opposite lists: gym and dance songs vs calm lofi and ambient tracks.
- **High-Energy Pop vs Deep Intense Rock:** they share Gym Hero, Block Party Anthem, and Storm Runner because all of them are high energy, but the rock listener's #1 is rock and the pop listener's #1 is pop. Genre decides the winner; energy fills the rest.
- **High-Energy Pop vs Sad but High-Energy:** both lists end with the same loud songs (Gym Hero, Block Party Anthem) because both want energy around 0.85–0.9, but the sad listener's #1 is a calm song, which shows genre + mood can override energy.
- **High-Energy Pop vs Unknown Genre:** both get Sunrise City and Rooftop Lights near the top because both like "happy," but the k-pop listener's scores are about 2 points lower because there is no genre match.
- **Chill Lofi vs Deep Intense Rock:** no songs in common at all. Calm, acoustic lofi vs loud, fast rock and metal. This is the clearest proof that the profile can tell "chill lofi" from "intense rock."
- **Chill Lofi vs Sad but High-Energy:** the only shared feeling is that both #1 songs are calm (Library Rain and Rainy Window), but for the sad listener that calm song is a mismatch on energy, while for the lofi listener it is a perfect fit.
- **Chill Lofi vs Unknown Genre:** no overlap. Lofi gets chill study songs; k-pop gets happy mid-energy songs. Mood and energy steer them apart even without a genre match for k-pop.
- **Deep Intense Rock vs Sad but High-Energy:** after their #1 songs, both lists are almost the same loud songs (Storm Runner, Gym Hero, Neon Pulse, Block Party Anthem), because once genre and mood stop matching, energy is the only thing left to rank by.
- **Deep Intense Rock vs Unknown Genre:** the rock listener gets very loud songs (energy around 0.9) and the k-pop listener gets medium songs (around 0.7). The energy target clearly shifts the list.
- **Sad but High-Energy vs Unknown Genre:** both are "tricky" listeners. The sad listener has one song that fits genre and mood (so a high #1 score of 3.40), while the k-pop listener has no genre match at all (top score only 1.94). Having even one matching song makes a big difference.

**Experiment I ran.** I halved the genre weight (2.0 → 1.0) and doubled the energy weight (1.0 → 2.0). Every listener kept the same #1 song, but positions 2–5 reshuffled. For the default pop listener, the happy song Rooftop Lights moved above the intense Gym Hero, which felt slightly more accurate. Details are in the README under "Experiments You Tried."

**Automated tests.** The two starter tests in `tests/test_recommender.py` pass: the pop/happy song ranks first for a pop/happy user, and every recommendation comes with a non-empty explanation.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
