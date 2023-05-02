from transformers import pipeline
import pandas as pd
#import matplotlib.pyplot as plt


sentiment_analysis = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")
comments = []
index = 0


def sentiment(comments):
    for comment in comments:
        index += 1
        content = comment.full_text
        sentiment = sentiment_analysis(content)
        comments.append({f'№{index}': content, 'sentiment': sentiment[0]['label']})

    df = pd.DataFrame(comments)
    sentiment_counts = df.groupby(['sentiment']).size()

    return sentiment_counts

#fig = plt.figure(figsize=(6,6), dpi=100)
#ax = plt.subplot(111)
#sentiment_counts.plot.pie(ax=ax, autopct='%1.1f%%', startangle=270, fontsize=12, label="")