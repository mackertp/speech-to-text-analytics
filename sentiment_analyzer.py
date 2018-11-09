"""
Scoring text files using the vader sentiment analyzer

@author Preston Mackert
"""

# ---------------------------------------------------------------------------------------------------- #
# imports
# ---------------------------------------------------------------------------------------------------- #

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
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


def get_most_neg(scored_files):
    inorder = sorted(scored_files)
    most_neg_score = inorder[0]
    most_neg_review = open("test_text/neg_reviews/" + scored_files[most_neg_score][0])
    return most_neg_review.readlines()


# ---------------------------------------------------------------------------------------------------- #
# main method
# ---------------------------------------------------------------------------------------------------- #

def main():
    folder_name = "test_text/neg_reviews/"
    sentiment_scores = read_and_score_text_files(folder_name)
    print(get_most_neg(sentiment_scores))


# ---------------------------------------------------------------------------------------------------- #
# call main
# ---------------------------------------------------------------------------------------------------- #

main()
