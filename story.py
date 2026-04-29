import re, random
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
    "Together, they stepped deeper into the unknown, ready for whatever came next.",

    # --- NEW EXPANDED LINES BELOW ---

    "A soft glow filtered through the branches above, casting shifting patterns across <char0>’s path.",
    "<char1> paused mid-step, sensing something watching them from the shadows.",
    "A distant hum vibrated through the ground, growing stronger with every heartbeat.",
    "<char0> brushed their fingers along the rough bark of an ancient tree, feeling warmth pulsing beneath it.",
    "The wind carried a whisper that almost sounded like a voice calling their name.",
    "<char2> emerged from behind a cluster of trees, their expression unreadable.",
    "<char1> knelt beside a cluster of strange flowers, each petal shimmering like tiny stars.",
    "A sudden flash of light streaked across the sky, leaving a trail that refused to fade.",
    "<char3> appeared at the edge of the clearing, clearly shaken by something unseen.",
    "<char0> felt the air thicken around them, as if the world was shifting into a different shape.",
    "A narrow stream wound across their path, glowing faintly as though lit from within.",
    "<char2> lowered their voice, warning the others to stay alert.",
    "The ground ahead split open just enough to reveal a faint, rhythmic pulse deep below.",
    "<char1> steadied <char0> as the air rippled unexpectedly around them.",
    "A faint trail of footprints appeared in the dirt, leading toward a place none of them recognized.",
    "<char3> studied the prints carefully, noting they didn’t belong to any creature they knew.",
    "<char0> felt a strange pressure in the air, like the moment before a storm breaks.",
    "A cluster of fireflies drifted past, moving in a pattern that seemed almost intentional.",
    "<char2> found a torn scrap of cloth snagged on a branch, its fabric unlike anything they’d seen.",
    "The forest grew unnaturally quiet, as if holding back a secret.",
    "<char1> motioned for everyone to stop, sensing something just beyond the treeline.",
    "A faint melody drifted through the air, haunting and beautiful.",
    "<char3> whispered that they had heard the song once before, long ago.",
    "<char0> felt the ground pulse beneath their feet, steady and rhythmic.",
    "A shimmering doorway flickered into existence before them, then vanished.",
    "<char2> reached out instinctively, trying to catch the fading light.",
    "The trees around them shifted subtly, forming a path that hadn’t existed moments earlier.",
    "<char1> took a cautious step forward, trusting the forest’s guidance.",
    "A warm glow spread across the horizon, signaling something awakening.",
    "<char0> sensed they were being watched, though they couldn’t tell from where.",
    "<char3> pointed to a distant silhouette moving slowly toward them.",
    "The air crackled with energy, raising the hairs on <char1>’s arms.",
    "A soft vibration hummed through the ground, resonating with the strange object <char0> carried.",
    "<char2> noticed symbols appearing faintly on their skin, glowing for only a moment.",
    "A gentle voice echoed through the clearing, though no one could see its source.",
    "<char0> felt a sudden surge of courage, stronger than anything they’d felt before.",
    "The wind shifted direction abruptly, carrying the scent of rain and something ancient.",
    "<char3> stepped closer to the group, determined not to be left behind.",
    "A faint outline of a structure appeared in the distance, shimmering like a mirage.",
    "<char1> recognized the shape from old stories, though they had never believed them.",
    "The path beneath their feet began to glow, guiding them forward.",
    "<char0> exchanged a hopeful glance with <char2>, knowing they were close to something important."
]


name_part1 = [
    "Ka", "Lo", "Mi", "Sa", "Ra", "El", "Fi", "No", "Ze",
    "Ari", "Va", "Li", "Ro", "Te", "Na", "Sol", "Jun", "Rei",
    "Ma", "Ori", "Ke", "Zan", "Lu", "Eri"
]

name_part2 = [
    "ra", "na", "lo", "mi", "ta", "ri", "sa", "vi", "ko",
    "len", "rin", "dor", "sha", "mon", "tis", "var", "lith",
    "wen", "sil", "mar", "dai", "rin", "vor"
]

starter_starts = []
starter_ends = []
starter_chain = marov_chains.build_markov_chain(story_starters, starter_starts, starter_ends)

body_starts = []
body_ends = []
body_chain = marov_chains.build_markov_chain(story_bodies, body_starts, body_ends)

def generate_story(text, length=20):
    text = text.lower()
    characters = extract_keywords(text)
    sentences = []

    start = marov_chains.generate_sentence(starter_chain, "", starter_starts, starter_ends)
    sentences.append(start)
    for _ in range(length - 1):
        sentences.append(marov_chains.generate_sentence(body_chain, "", body_starts, body_ends))

    sentences = add_characters(sentences, characters)
    return " ".join(sentences)

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

def add_characters(story_list, characters):
    new_list = []
    for sent in story_list:
        strs = re.findall(r"<char(\d+)>", sent)
        for s in strs:
            num = int(s)
            while len(characters) <= num:
                characters.append(generate_random_character())
            sent = sent.replace(f"<char{num}>", characters[num])
        new_list.append(sent)
    return new_list

def generate_random_character():
    return random.choice(name_part1) + random.choice(name_part2)