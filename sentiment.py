from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

nltk.data.path.append('nltk_data/')

sia = SentimentIntensityAnalyzer()

def sentimentfunc(text):

    score = sia.polarity_scores(text)

    for k in score:
        score[k] = round(score[k]*100,2)

    return score

if __name__ == "__main__":
    print(sentimentfunc("i am happy"))


