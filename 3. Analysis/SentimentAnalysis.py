import pandas as pd
#import nltk
#from nltk.sentiment.vader import SentimentIntensityAnalyzer
#nltk.download('vader_lexicon')
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

reviews = pd.read_csv('C:/Users/Hiran/Desktop/virtual_workspace/demo_project/Reviews_combined_cleaned.csv',header=None)
reviews.columns = ['Website', 'Category', 'Attraction_name', 'place', 'Heading', 'Review_text', 'Review_date', 'Review_rating', 'review_id', 'attraction_id']

def vader_sentiment(sentence):
    sentiment = SentimentIntensityAnalyzer()
    score = sentiment.polarity_scores(sentence)
    return score

vader_results = [vader_sentiment(row) for row in reviews['Review_text']]
results_df = pd.DataFrame(vader_results)
#text_df = pd.DataFrame(reviews, columns = ['text'])
reviews = reviews.join(results_df)
#reviews['Weighted_Rating'] = reviews['compound'] * reviews['Rating']
reviews.to_csv('C:/Users/Hiran/Desktop/virtual_workspace/demo_project/Reviews_Sentiments.csv')