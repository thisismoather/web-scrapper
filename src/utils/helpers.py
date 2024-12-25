def split_sentences(text):
    import re
    return re.split(r'(?<=[.!?]) +', text)

def match_countries(text, country_list):
    matches = []
    for country in country_list:
        if country.lower() in text.lower():
            matches.append(country)
    return matches

def extract_offshore_words(sentence, offshore_words):
    found_words = []
    for word in offshore_words:
        if word.lower() in sentence.lower():
            found_words.append(word)
    return found_words