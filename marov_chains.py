#markov_chains.py
import random

#LLM Sentences
training_sets = {
    "greeting": [
        "Hello! Nice to see you.",
        "Hi there, how can I help?",
        "Hey! Hope you're doing well.",
        "Good to see you today.",
        "Greetings! How can I assist you?",
        "Hello! I hope you're having a great day.",
        "Hi! It's a pleasure to meet you.",
        "Good morning! How can I be of service?",
        "Hello! How are you feeling today?",
        "Hi! Let me know if you need anything.",
        "Hey there, it's great to hear from you.",
        "Yo! What's going on today.",
        "Howdy! What can I do for you.",
        "Nice to see you again.",
        "Hey friend, how are things going.",
        "Hi again, what’s up.",
        "Hey dude, how’s your day going.",
        "Good afternoon! How can I help you today."
    ],

    "feeling_bored": [
        "Sounds like you're bored.",
        "Maybe we can find something fun to do.",
        "I get it, boredom happens.",
        "Want to try something interesting.",
        "Would you like some suggestions to pass the time.",
        "Sometimes a new activity can help.",
        "Want to hear a joke or a short story.",
        "Let's find something engaging together.",
        "Is there something specific you'd like to explore.",
        "I'm here to make things more interesting for you.",
        "We can try something new if you'd like.",
        "Maybe a small challenge could help break the boredom.",
        "If you're bored, we can talk about anything you want.",
        "Let’s switch things up a bit."
    ],

    "goodbye": [
        "Talk to you later.",
        "See you soon.",
        "Goodbye for now.",
        "Catch you later.",
        "It was nice talking to you.",
        "Take care and have a great day.",
        "Until next time, goodbye.",
        "Feel free to reach out again.",
        "Wishing you a wonderful day ahead.",
        "Goodbye! Looking forward to our next chat.",
        "See you next time.",
        "I'll be here whenever you want to talk again.",
        "Have a good rest of your day."
    ],

    "help": [
        "I'm here to help you.",
        "Let me know what you need.",
        "I'm glad to help with that.",
        "Feel free to ask anything.",
        "How can I assist you today.",
        "I'm here to support you.",
        "Please tell me how I can be of help.",
        "I'm happy to provide assistance.",
        "Just let me know what you'd like to do.",
        "I'm here to make things easier for you.",
        "If you need anything, I'm right here.",
        "Tell me what you're trying to do and I’ll help."
    ],

    "thank_you": [
        "You're very welcome.",
        "Happy to help.",
        "No problem at all.",
        "Glad I could assist.",
        "Anytime! Let me know if you need more help.",
        "You're welcome! Feel free to ask anything else.",
        "My pleasure.",
        "I'm here whenever you need me.",
        "Thank you for reaching out.",
        "Always happy to help.",
        "You're welcome, glad I could help you today."
    ],

    "apology": [
        "I'm sorry for any inconvenience.",
        "Please accept my apologies.",
        "Sorry if I caused any confusion.",
        "I apologize for that.",
        "Thank you for your patience.",
        "Sorry about that, let me assist you better.",
        "I appreciate your understanding.",
        "Sorry if I missed anything.",
        "I'm here to make things right.",
        "Please let me know how I can improve.",
        "My apologies, let me try again."
    ],

    "confirmation": [
        "Yes, that's correct.",
        "Exactly.",
        "You're right.",
        "That's what I thought.",
        "Absolutely.",
        "Correct, I understand.",
        "Yes, I agree.",
        "That's right.",
        "Precisely.",
        "Indeed.",
        "Yep, that matches what I know.",
        "That’s correct, you’ve got it."
    ],

    "negation": [
        "I'm sorry, I can't do that.",
        "Unfortunately, that's not possible.",
        "I'm afraid I can't help with that.",
        "Sorry, I don't have the information.",
        "That's not something I can assist with.",
        "I apologize, but I can't do that.",
        "Sorry, I don't understand that request.",
        "Regrettably, I can't help with that.",
        "That's outside my capabilities.",
        "Sorry, I can't assist with that right now.",
        "I wish I could help, but I can’t do that."
    ],
    "fallback": [
        "I'm here if you want to talk about anything.",
        "That sounds interesting, tell me more.",
        "I'm not totally sure what you meant, but I'm listening.",
        "Feel free to explain it a bit more.",
        "I'm here to chat about whatever’s on your mind.",
        "Tell me more about that.",
        "I’m curious what you meant by that.",
        "I’m here with you, go on.",
        "That caught my attention, what else is going on.",
        "I’m following along, keep going.",
        "I’m here to talk about anything you want.",
        "You can tell me more if you’d like.",
        "I’m trying to understand, say a little more.",
        "I’m here and ready to chat.",
        "Whatever you want to talk about, I’m here.",
        "I’m listening, go ahead.",
        "That sounds like something worth talking about.",
        "I’m here to hear whatever you want to share.",
        "You can tell me anything that’s on your mind.",
        "I’m here to keep the conversation going with you."
    ]
}


#Markov Chain Builder
def build_markov_chain(text_list, start_words, end_words):
    chain = {}
    
    for sentence in text_list:
        words = sentence.split()
        start_words.append(words[0])
        end_words.append(words[-1])
        for i in range(len(words) - 1):
            word = words[i]
            next_word = words[i + 1]
            if word not in chain:
                chain[word] = []
            chain[word].append(next_word)
    return chain

#Generate New Sentences
def generate_sentence(chain, intent, start_words, end_words, length=12):
    word = random.choice(start_words)
    sentence = [word]

    for _ in range(length - 1):
        if word in chain:
            next_word = random.choice(chain[word])
            sentence.append(next_word)
            word = next_word
            if word in end_words and len(sentence) > 6:
                break
        else:
            break
    return " ".join(sentence)