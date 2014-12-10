# FILE: dict.py 
# ---------------------------------
# Testing module for pickle dictionary

import pickle, sys

def rhyme(word1, word2):

    if word1 not in d or word2 not in d:
        # heuristic, safe to take slice if len < 3
        return (word1[-3:] == word2[-3:] and word1 != word2)
    else:
        if d[word1][0] == d[word2][0]:
            return False
        if d[word1][1] == d[word2][1]:
            return True
        else:
            return False

filename = open("new_word_data.p", "rb")
d = pickle.load()

# rhymecount = {}
# for word in d.keys():
# 	counter = 0
# 	for word2 in d.keys():
# 		if rhyme(word, word2):
# 			counter += 1
# 	rhymecount[word] = counter
# 	print word, counter


pickle.dump(d, open("new_new_word_data.p", "wb"), 2)

#print isNotPrepOrArticle(sys.argv[1]), d[sys.argv[1]]