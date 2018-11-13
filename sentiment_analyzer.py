"""
Methods that utilize the vader sentiment analyzer and perform text analysis on a batch of files. For
the sake of a proof of concept currently using negative movie reviews as the base data set

@author Preston Mackert
"""

# ---------------------------------------------------------------------------------------------------- #
# imports
# ---------------------------------------------------------------------------------------------------- #

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wtforms import Form, StringField, SelectField
from fuzzywuzzy import fuzz
import os
import operator

# ---------------------------------------------------------------------------------------------------- #
# global variables for the sentiment analyzer by vader, and also storing all of the text from files
# so that we can analyze it and access it without passing through browser
# ---------------------------------------------------------------------------------------------------- #

analyzer = SentimentIntensityAnalyzer()
text_db = {}


# ---------------------------------------------------------------------------------------------------- #
# support methods
# ---------------------------------------------------------------------------------------------------- #

def sentiment_analyzer_scores(sentence):
    score = analyzer.polarity_scores(sentence)
    return score


def read_and_score_text_files(folder_name):
    folder = os.listdir(folder_name)
    scores = {}
    for file in folder:
        try:
            review = open(folder_name+file).readlines()
            text_db.update({file: review})
            for line in review:
                    score = sentiment_analyzer_scores(line)
                    score = score["compound"]
                    if score in scores.keys():
                        scores[score].append(file)
                    else:
                        scores[score] = [file]
        except:
            continue
    return scores


def get_20_most_neg_files(scored_files):
    inorder = sorted(scored_files)
    files = {}
    count = 0
    pos = 0
    while count < 20:
        score = inorder[pos]
        for file in scored_files[score]:
            files[file] = score
            count += 1
        pos += 1
    return files


def search_files(keyphrase):
    table_data = {}
    for file in text_db:
        text = text_db[file]
        for line in text:
            for word in line.split(" "):
                if fuzz.ratio(keyphrase, word) >= 75:
                    if file in table_data.keys():
                        table_data[file].append(fuzz.ratio(keyphrase, word))
                    else:
                        table_data[file] = [fuzz.ratio(keyphrase, word)]
    return table_data


def sort_search(data):
    file_scores = {}
    for file in data:
        num_files = len(data[file])
        avg_score = sum(data[file])/num_files
        composite = num_files+avg_score
        file_scores.update({file: composite})
    return sorted(file_scores.items(), key=operator.itemgetter(1), reverse=True)

# ---------------------------------------------------------------------------------------------------- #
# main method
# ---------------------------------------------------------------------------------------------------- #
""""
def main():
    folder_name = "test_text/neg_reviews/"
    sentiment_scores = read_and_score_text_files(folder_name)
    print(get_20_most_neg_files(sentiment_scores))


# ---------------------------------------------------------------------------------------------------- #
# call main
# ---------------------------------------------------------------------------------------------------- #

main()
"""
