import enchant
d = enchant.Dict("en_US")

def reportNonWords(text):
    nonWords = []
    textArr = text.split()
    for word in textArr:
        if not d.check(word):
            nonWords.append(word)
    return [text, nonWords]
