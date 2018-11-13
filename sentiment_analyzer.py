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
import os

# ---------------------------------------------------------------------------------------------------- #
# instantiate vader's analyzer tool
# ---------------------------------------------------------------------------------------------------- #

analyzer = SentimentIntensityAnalyzer()


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


# ---------------------------------------------------------------------------------------------------- #
# main method
# ---------------------------------------------------------------------------------------------------- #
"""
def main():
    folder_name = "test_text/neg_reviews/"
    sentiment_scores = read_and_score_text_files(folder_name)
    print(get_20_most_neg_files(sentiment_scores))


# ---------------------------------------------------------------------------------------------------- #
# call main
# ---------------------------------------------------------------------------------------------------- #

main()
"""
