# importing libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

st.title("Sentiment Analysis")
st.sidebar.title("Toolbar")

st.markdown("## US Airlines Tweets")
st.markdown("### To view the charts, navigate to the sidebar and untick "Hide"")
st.sidebar.markdown("This app is a Streamlit Dashboard for Sentiment Analysis")


@st.cache(persist=True)
def load_data():
    data = pd.read_csv("Tweets.csv")
    data["tweet_created"] = pd.to_datetime(data["tweet_created"])
    return data


data = load_data()

# to show random -ve, +ve, neutral tweets
st.sidebar.subheader("Show random tweet")
random_tweet = st.sidebar.radio("Sentiment:", ("positive", "neutral", "negative"))
st.sidebar.markdown(data.query("airline_sentiment == @random_tweet")[["text"]].sample(n=1).iat[0,0])

# Visualization
st.sidebar.markdown("### Number of tweets as per sentiment")
st.sidebar.markdown("#### Uncheck the box for viewing the visualisation")
select = st.sidebar.selectbox("Visualization type:", ["Histogram","Pie chart"], key = "1")

sentiment_count = data["airline_sentiment"].value_counts()
sentiment_count = pd.DataFrame({"Sentiment":sentiment_count.index, "Tweets":sentiment_count.values})

#choice b/w hist and pie
if not st.sidebar.checkbox("Hide", True):
    st.markdown("### Number of tweets as per sentiment")
    if select == "Histogram":
        fig = px.bar(sentiment_count,x="Sentiment",y="Tweets",color="Tweets",height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values ="Tweets",names="Sentiment")
        st.plotly_chart(fig)

#bar charts per airline per sentiment
st.sidebar.subheader("Break airline tweets by sentiment")
choice = st.sidebar.multiselect("Pick the airlines:",("US Airways","United","American","Southwest","Delta","Virgin America"),key="0")

if len(choice)>0:
    choice_data = data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data,x="airline",y="airline_sentiment",histfunc="count",color="airline_sentiment",facet_col="airline_sentiment",labels={"airline_sentiment":"tweets"},height=600,width=800)
    st.plotly_chart(fig_choice)

#wordcloud
st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio("Display word cloud as per the following sentiment:",("positive","neutral","negative"))
if not st.sidebar.checkbox("Close",True,key="3"):
    st.header("Word cloud for %s sentiment"%(word_sentiment))
    df=data[data["airline_sentiment"]==word_sentiment]
    words= " ".join(df["text"])
    processed_words = " ".join([word for word in words.split() if "http" not in word and not word.startswith("@") and word != "RT"])
    wordcloud = WordCloud(stopwords=STOPWORDS,background_color="white",height=640,width=800).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()
    st.set_option('deprecation.showPyplotGlobalUse', False)

