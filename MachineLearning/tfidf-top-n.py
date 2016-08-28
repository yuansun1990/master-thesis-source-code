import csv
from sets import Set
import nltk
import string
import os, sys
import numpy as np
from nltk.stem import WordNetLemmatizer, PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

"""tfidf-top-n.py: select features (tokens with top 30 tfidf values) and generate a features list"""
__author__ = "YuanSun"


def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = []
    for word in tokens:
        stems.append(_wnl.lemmatize(word))
        #if _wnl.lemmatize(word).endswith('e') else _porter.stem(word))
    return stems

# main
def main(input_path, output_file):
    # tokenize
    token_dict = {}
    for dirpath, dirs, files in os.walk(input_path):
        for f in files:
            fname = os.path.join(dirpath, f)
            with open(fname) as pearl:
                text = pearl.read()
                token_dict[f] = text.lower().translate(None, string.punctuation)

    tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
    tfs = tfidf.fit_transform(token_dict.values())

    feature_names = tfidf.get_feature_names()
    n = tfs.shape[0]        # number of labels

    top_words, top_words_set = [], Set([])
    additional_features = [ '?', '@', '!', '$', 'number', 'url' ]
    for i in range(n):
        tfidf_map = np.array([ [feature_names[col], tfs[i, col]] for col in tfs[i].nonzero()[1] if feature_names[col] not in additional_features ])
        for word_tuple in tfidf_map[tfidf_map[:,1].argsort()[::-1]][:30]:
            if word_tuple[0] not in top_words_set:
                top_words.append(word_tuple)
                top_words_set.add(word_tuple[0])

    for feature in additional_features:
        top_words.append([feature, 0])

    with open(output_file, 'w') as f:
        a = csv.writer(f, delimiter=',')
        a.writerows(top_words)

if __name__ == '__main__':
    _porter = PorterStemmer()
    _wnl = WordNetLemmatizer()

    main(sys.argv[1], sys.argv[2])
