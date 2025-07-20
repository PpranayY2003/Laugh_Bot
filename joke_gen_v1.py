import pandas as pd

# Try this for both files one by one
df_sent = pd.read_csv("transcripts_with_sentiment.csv")
df_topic = pd.read_csv("documents_with_named_topics.csv")

print("Sentiment columns:", df_sent.columns)
print("Topic columns:", df_topic.columns)


merged_df = pd.merge(df_sent, df_topic[['cleaned_text', 'Named_Topic']], on='cleaned_text', how='inner')

# Rename columns for consistency
merged_df = merged_df.rename(columns={
    "Named_Topic": "topic_label",
    "tb_label": "sentiment"
})

# Save the final dataset
merged_df.to_csv("final_topic_sentiment.csv", index=False)


df = pd.read_csv("final_topic_sentiment.csv")

import streamlit as st
import pandas as pd
import random

# Load the correct CSV file
df = pd.read_csv("documents_with_named_topics.csv")  # or merged CSV if already done
sentiment_df = pd.read_csv("transcripts_with_sentiment.csv")

# Merge both if not already merged
df = pd.merge(df, sentiment_df[["cleaned_text", "tb_label"]], on="cleaned_text", how="inner")
df.rename(columns={"Named_Topic": "topic_label", "tb_label": "sentiment"}, inplace=True)

# Streamlit UI
st.set_page_config(page_title="Joke Recommender", layout="centered")
st.title("😂 Joke Recommender by Topic")
st.markdown("Type a topic (like `politics`, `therapy`, `relationship`) to get a related joke.")

# Text input
user_input = st.text_input("🎯 Which topic are you in the mood for?", "")

# Sentiment filter
sentiment_choice = st.selectbox("🙂 Select sentiment (optional)", ["Any", "positive", "negative", "neutral"])

# Joke generation
if st.button("Tell me a joke!"):
    topic_input = user_input.strip().lower()
    filtered_df = df.copy()

    if topic_input:
        filtered_df = filtered_df[filtered_df["topic_label"].str.lower() == topic_input]

    if sentiment_choice != "Any":
        filtered_df = filtered_df[filtered_df["sentiment"].str.lower() == sentiment_choice]

    if not filtered_df.empty:
        joke = filtered_df["cleaned_text"].sample(1).values[0]
        st.success(joke)
    else:
        st.warning("😕 No jokes found for that topic/sentiment. Try a different one!")

# Show available topics
with st.expander("📚 See available topics"):
    st.write(", ".join(sorted(df["topic_label"].unique())))
