import re
import marov_chains

story_starters = [
    "Once upon a time, <char0> found themselves standing at the edge of a quiet forest.",
    "In a small forgotten town, something unusual began to stir.",
    "Long ago, before anyone kept records, a strange event changed everything.",
    "On a calm morning, <char0> noticed the sky looked different than usual.",
    "Far beyond the familiar roads, a hidden path waited to be discovered.",
    "In a world where ordinary rules didn’t always apply, a new story began.",
    "Deep in the heart of an ancient valley, a secret waited to be uncovered.",
    "Nobody knew why the old clock tower started ticking again, but it did.",
    "At the break of dawn, a soft glow spread across the hills, signaling the start of something unexpected.",
    "Legends spoke of a moment like this, though few believed it would ever come.",
    "The wind carried a whisper that only <char0> seemed able to hear.",
    "In a quiet corner of the world, a mystery slowly came to life.",
    "The day began like any other, until a single choice changed its course.",
    "Hidden beneath layers of dust and time, an old map revealed its first clue.",
    "No one could explain the strange footprints that appeared overnight.",
    "As the sun dipped below the horizon, the adventure quietly began.",
    "The village had seen many odd things, but nothing quite like this.",
    "A gentle rumble echoed through the ground, hinting at something awakening.",
    "For reasons no one understood, the stars shone brighter that night.",
    "It all started when <char0> opened a door that wasn’t supposed to exist."
]

story_bodies = [
    "<char0> walked carefully through the quiet path, unsure what waited ahead.",
    "A faint sound echoed from somewhere beyond the trees, drawing <char0> closer.",
    "Without warning, <char1> appeared from behind an old stone wall.",
    "The air shimmered for a moment, as if the world itself was holding its breath.",
    "<char0> noticed strange markings carved into the ground, glowing softly.",
    "A gentle breeze carried the scent of something unfamiliar through the air.",
    "<char1> hesitated before speaking, unsure how <char0> would react.",
    "Far in the distance, a warm light flickered like a signal calling them forward.",
    "The path twisted unexpectedly, revealing a hidden clearing no one had seen before.",
    "<char0> felt a sudden rush of curiosity, stronger than any fear.",
    "A quiet rustling came from the bushes, and both of them froze.",
    "The sky above shifted colors, hinting that something magical was unfolding.",
    "<char1> offered a small smile, trying to ease the tension between them.",
    "They continued walking until the trees opened into a wide, peaceful meadow.",
    "A mysterious object lay half-buried in the dirt, pulsing with a soft glow.",
    "<char0> reached out to touch it, feeling a strange warmth spread through their hand.",
    "The ground trembled slightly, as if reacting to their presence.",
    "<char1> stepped forward, determined to uncover the truth behind the strange events.",
    "A distant roar echoed across the landscape, sending chills down their spines.",
    "Despite the uncertainty, <char0> felt a spark of hope guiding them onward.",
    "They exchanged a determined glance, knowing the journey had only just begun.",
    "The forest around them seemed alive, whispering secrets they couldn’t quite understand.",
    "<char1> pointed toward a narrow trail that hadn’t been there moments before.",
    "The air grew warmer as they approached a hidden cave entrance.",
    "<char0> sensed that whatever lay inside would change everything.",
    "A soft glow illuminated the cave walls, revealing ancient symbols.",
    "<char1> brushed dust from an old stone tablet, uncovering a forgotten message.",
    "The message hinted at a power long lost, waiting to be awakened.",
    "<char0> felt a strange connection to the symbols, as if they were meant to find them.",
    "Together, they stepped deeper into the unknown, ready for whatever came next."
]

starter_starts = []
starter_ends = []
starter_chain = marov_chains.build_markov_chain(story_starters, starter_starts, starter_ends)

body_starts = []
body_ends = []
body_chain = marov_chains.build_markov_chain(story_bodies, body_starts, body_ends)

def generate_story(text):
    text = text.lower()
    characters = extract_keywords(text)

    start = marov_chains.generate_sentence(starter_chain, "", starter_starts, starter_ends)
    return start

def extract_keywords(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)

    stopwords = {
        "tell", "me", "a", "an", "the", "story", "about", "make",
        "create", "write", "please", "can", "you", "could", "and",
        "with", "in", "on", "at", "to", "from", "for", "of", "by",
        "as", "is", "was", "were", "it", "that"
    }

    # Common adjectives you want to support
    adjectives = {
        "smart", "brave", "tiny", "lonely", "ancient", "mysterious",
        "ruined", "lost", "forgotten", "strange", "quiet", "dark",
        "golden", "broken", "wild", "gentle", "sleepy", "massive",
        "small", "big", "old", "young", "shy", "proud"
    }

    # Fallback rule: words that *look* descriptive
    adj_endings = ("y", "ful", "less", "ous", "ive", "al", "ic", "ish")

    words = [w for w in text.split() if w not in stopwords]

    keywords = []
    i = 0

    while i < len(words):
        w = words[i]

        # Check if it's an adjective by list OR by ending
        is_adj = (w in adjectives) or w.endswith(adj_endings)

        if is_adj and i + 1 < len(words):
            # Pair adjective + noun
            pair = w + " " + words[i + 1]
            keywords.append(pair)
            i += 2
        else:
            keywords.append(w)
            i += 1

    return keywords
