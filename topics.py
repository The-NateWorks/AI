# topics.py
import marov_chains
topic_sets = {
    "emotion": [
        "It sounds like you're dealing with some feelings.",
        "Emotions can be confusing sometimes.",
        "If something’s on your mind, I’m here to listen.",
        "It’s okay to feel that way.",
        "Everyone has moments like that.",
        "You’re not alone in how you feel.",
        "Talking about it can sometimes help.",
        "Feelings can change quickly, and that’s normal.",
        "If you want to share more, I’m here.",
        "It’s totally valid to feel that way."
    ],

    "math": [
        "Math questions can be fun to solve.",
        "Let me think through that problem.",
        "Numbers make things interesting.",
        "Math is all about patterns.",
        "I can help break the problem down.",
        "Let’s figure this out step by step.",
        "Math can be tricky, but we’ll get it.",
        "I like solving problems like this.",
        "Let’s work through the numbers.",
        "Math is basically a puzzle."
    ],

    "time": [
        "Time really does move fast.",
        "The day can change before you know it.",
        "Every hour feels different depending on what you're doing.",
        "Time of day can totally change the vibe.",
        "Sometimes the day feels slow, sometimes fast.",
        "The clock keeps going no matter what.",
        "Time can feel weird sometimes.",
        "Every moment is a new chance to do something.",
        "The day has its own rhythm.",
        "It’s interesting how time feels different depending on your mood."
    ],

    "day": [
        "Every day has its own energy.",
        "Some days feel long, others fly by.",
        "I hope today has been treating you well.",
        "Days can be unpredictable sometimes.",
        "A new day always brings new chances.",
        "Some days are easier than others.",
        "The day can change depending on what you do.",
        "I hope your day has had some good moments.",
        "Every day is different in its own way.",
        "Today is another step forward."
    ],

    "help": [
        "I’m here to support you however I can.",
        "Just tell me what you need help with.",
        "I’ll do my best to assist you.",
        "You don’t have to figure everything out alone.",
        "I’m ready whenever you are.",
        "Let’s solve this together.",
        "I’m here to make things easier.",
        "Whatever you need, I’ll try to help.",
        "You can count on me for support.",
        "I’m here to guide you through it."
    ],

    "confusion": [
        "Let me try to make things clearer.",
        "It’s okay to be confused sometimes.",
        "I can explain it in a simpler way.",
        "Let’s break it down together.",
        "Confusion just means you’re learning.",
        "I’ll try to explain it differently.",
        "No worries, we can go step by step.",
        "It’s normal to not understand something right away.",
        "Let me help clear things up.",
        "We can figure it out together."
    ],

    "social": [
        "It’s always nice talking with you.",
        "I’m glad you’re here.",
        "I enjoy chatting with you.",
        "It’s good to hear from you again.",
        "I’m always here to talk.",
        "Conversations make the day better.",
        "I like keeping the conversation going.",
        "It’s cool getting to talk with you.",
        "I’m here whenever you want to chat.",
        "Talking with you is always nice."
    ]
}

topic_chains = {}
topic_starts = {}
topic_ends = {}
for topic, set in topic_sets.items():
    topic_starts[topic] = []
    topic_ends[topic] = []
    topic_chains[topic] = marov_chains.build_markov_chain(set, topic_starts[topic], topic_ends[topic])

def flair_topic(topic, intent):
    topic_flair = ""
    if topic in topic_chains:
        topic_flair = marov_chains.generate_sentence(topic_chains[topic], topic, topic_starts[topic], topic_ends[topic])
    else:
        topic_flair = ""
    return topic_flair