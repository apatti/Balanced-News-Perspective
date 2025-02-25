
import streamlit as st
from agents.viewpointRetriever import getNews
import dotenv
dotenv.load_dotenv()

st.title("Balanced News Perpective")
st.write("An innovative tool designed to provide users with diverse perspectives on news headlines.")
st.write(" The app takes a headline as input and delivers three distinct views: right-leaning, left-leaning, and center/unbiased. By presenting these perspectives, the app ensures users gain a well-rounded understanding of the news, fostering critical thinking and informed discussions.")
headLine = st.text_input("Enter a news headline:")
st.button("Get Balanced News Perspective")
getNews(headLine)
