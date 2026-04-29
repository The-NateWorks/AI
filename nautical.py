# main.py
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import random, datetime, importlib
import topics, marov_chains, story, search
importlib.reload(story)
importlib.reload(marov_chains)
#Memory
memory = {}
last_user = None
last_bot = None


def this_and_that(text):
    out = []
    for i in range(len(text.split()) - 1):
        out.append(text.split()[i] + " " + text.split()[i + 1])
    return out



#Training Data Load
data = pd.read_csv("training_data.csv")
training_sentences = data["text"].tolist()
training_labels = data["intent"].tolist()
training_topics = data["topic"].tolist()

#Convert Text to Numbers
vectorize = CountVectorizer()
X = vectorize.fit_transform(training_sentences)

#AI Model
model = MultinomialNB()
model.fit(X, training_labels)

topic_model = MultinomialNB()
topic_model.fit(X, training_topics)

#Predictor
def predict_intent(text):
    X_test = vectorize.transform([text])
    return model.predict(X_test)[0]
def predict_topic(text):
    X_test = vectorize.transform([text])
    return topic_model.predict(X_test)[0]
def predict_next_intent(bot_reply):
    X_test = vectorize.transform([bot_reply])
    return model.predict(X_test)[0]
def predict_topic_with_confidence(text):
    X_test = vectorize.transform([text])
    probs = topic_model.predict_proba(X_test)[0]
    labels = topic_model.classes_
    
    best_index = probs.argmax()
    best_topic = labels[best_index]
    confidence = probs[best_index]
    
    return best_topic, confidence


#Blender
def blend_response(intent, topic, main_sentence, topic_conf):
    parts = []

    parts.append(main_sentence)
    if topic_conf >= 0.55 and topic in topics.topic_sets:
        parts.append(random.choice(topics.topic_sets[topic]))
    parts.append(topics.flair_topic(topic, intent))

    parts = [p for p in parts if p.strip()]
    return " ".join(parts)

#Response
def respond(user_input):
    global last_user, last_bot
    text = user_input.lower()

    topic, topic_conf = predict_topic_with_confidence(user_input)

    math_words = ["plus", "minus", "times", "multiplied", "divide", "divided", "over", "sum of", "the sum of"]
    math_symbols = ["+", "-", "*", "/", "(", ")"]

    if text in ["what", "what?", "huh", "??", "???", "i don't understand", "im confused", "i'm confused"]:
        intent = "misunderstanding"
    elif any(w in text for w in math_words) or any(sym in text for sym in math_symbols):
        intent = "ask_math"
        topic = "math"
    elif (any(wrd in ["search", "look up", "find", "who is"] for wrd in text.split()) or
        any(phr in ["search", "look up", "find", "who is"] for phr in this_and_that(text))
    ):
        intent = "search"
        topic = "search"
    else:
        intent = predict_intent(user_input)

    topic_flair = topics.flair_topic(topic, intent)

    if "name" in memory and memory["name"] == "Jax":
        main = marov_chains.generate_sentence(chains["comp_jax"], "comp_jax", start_words["comp_jax"], end_words["comp_jax"])
        topic = ""
    elif intent in chains:
        main =  marov_chains.generate_sentence(chains[intent], intent, start_words[intent], end_words[intent])

    elif intent == "misunderstanding":
        if last_bot:
            last_intent = predict_intent(last_bot)
            if last_intent in chains:
                simple = marov_chains.generate_sentence(chains[last_intent], last_intent, start_words[intent], end_words[intent])
                main = f"I said: '{last_bot}'. Let me explain it more clearly.\n{simple}"
            else:
                main = f"I said: '{last_bot}'."
        else:
            main = "Sorry about that. What part are confused on"

    # Asking name
    elif intent == "ask_name":
        main = "I'm Nautical."

    # Setting name
    elif intent == "set_name":
        name = extract_name(user_input)
        if name:
            memory["name"] = name
            main = f"Nice to meet you, {name}"
        else:
            main = "I'm sorry I didn't catch that. Could you say it again?"
    
    #Getting name
    elif intent == "get_name":
        if "name" in memory:
            main = f"Your name is {memory['name']}."
        else:
            main = "You haven't told me your name yet."

    elif intent == "ask_math":
        main = solve_math(user_input)

    elif intent == "get_day":
        main = f"Today is {datetime.datetime.now().strftime('%A %B %-d, %Y')}."
    elif intent == "get_time":
        main = f"It is currently {datetime.datetime.now().strftime('%-I:%M %p')}."
    elif intent == "story":
        main = story.generate_story(user_input)
    elif intent == "search":
        main = search.search(search.extract_search_query(user_input))
    
    # Unknown intent
    else:
        main = marov_chains.generate_sentence(chains["fallback"], intent, start_words["fallback"], end_words["fallback"])
    
    bot_reply = blend_response(intent, topic, main, topic_conf)

    last_user = user_input
    last_bot = bot_reply
    return bot_reply

#Math
def solve_math(text):
    try:
        expr = text.lower()
        fillers = [
            "what is", "what's", "can you tell me", "please", 
            "solve", "calculate", "the answer to", "?", "equals", "equal to", "the sum of"
        ]
        for f in fillers:
            expr = expr.replace(f, "")

        if "sum" in text:
            expr = expr.replace("and", "+")

        ops = {
            "plus": "+",
            "add": "+",
            "minus": "-",
            "subtract": "-",
            "times": "*",
            "multiplied by": "*",
            "multiply": "*",
            "x": "*",
            "divided by": "/",
            "divide": "/",
            "over": "/"
        }
        
        for word, symbol in ops.items():
            expr = expr.replace(word, symbol)

        numbers = {
            "zero": "0", "one": "1", "two": "2", "three": "3",
            "four": "4", "five": "5", "six": "6", "seven": "7",
            "eight": "8", "nine": "9", "ten": "10"
        }
        for word, digit in numbers.items():
            expr = expr.replace(word, digit)

        expr = expr.strip()
        
        answer = eval(expr)

        return f"The answer is {answer}."
    except:
        return "I'm not sure how to do that yet."

#Name
def extract_name(text):
    text = text.lower()
    patterns = [
        "my name is ",
        "i am ",
        "i'm ",
        "call me ",
        "you can call me ",
        "this is "
    ]

    for p in patterns:
        idx = text.find(p)
        if idx != -1:
            start = idx + len(p)
            name = text[start:].strip()
            name = name.split()[0]
            return name.title()
    return None

#Generate Markov Chain For Each Intent
chains = {}
start_words = {}
end_words = {}
for  intent, text_list in marov_chains.training_sets.items():
    start_words[intent] = []
    end_words[intent] = []
    chains[intent] = marov_chains.build_markov_chain(text_list, start_words[intent], end_words[intent])
