from better_profanity import profanity

profanity.load_censor_words()

def contains_prohibited_words(text):
    return profanity.contains_profanity(text)
