import requests
import json
import os
import time
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import re
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="LinkedIn Sentiment Analysis", layout="wide")
purl="https://www.linkedin.com/in/williamhgates/"

def scrapeposts():
    api_url="https://fresh-linkedin-profile-data.p.rapidapi.com/get-profile-posts"
    querystring = {"linkedin_url":{purl},"type":"posts"}
    headers = {
        "X-RapidAPI-Key": os.getenv("RAPID_API_KEY"),
        "X-RapidAPI-Host": "fresh-linkedin-profile-data.p.rapidapi.com"
    }
    api_res = requests.get(api_url, headers=headers, params=querystring)
    
    if api_res.status_code == 200:
        json_data = json.loads(api_res.text)
        data = json_data['data'][:10]
        
        post_urls = [item['post_url'] for item in data]
        num_likes = [item['num_likes'] for item in data]
        num_comments = [item['num_comments'] for item in data]
        num_reposts = [item['num_reposts'] for item in data]
        
        st.divider()

        p1,p3,p4 = st.columns(3)
        with p1:
            st.write("Total Likes")
            st.title(sum(num_likes))
            st.divider()
        with p3:
            st.write("Total Impressions")
            total_impressions = sum(num_likes)+sum(num_reposts)
            st.title(total_impressions)
            st.divider()
        with p4:
            st.write("Total Engagements")
            total_engagements = sum(num_likes)
            st.title(total_engagements)
            st.divider()

        df = pd.DataFrame({
            'Post URL': post_urls,
            'Number of Likes': num_likes,
            'Number of Comments': num_comments,
            'Number of Reposts': num_reposts,
        })

        df1 = pd.DataFrame({
            'Number of Likes': num_likes,
        })
        df2 = pd.DataFrame({
            'Number of Comments': num_comments,
        })
        df4 = pd.DataFrame({
            'Number of Reposts': num_reposts,
        })

        part1,part2 = st.columns(2)
        with part1:
            st.bar_chart(data = df1, y = "Number of Likes")
        with part2:
            st.bar_chart(data = df2, y = "Number of Comments")

        st.title("Last 10 Posts:")
        st.table(df)

        df5 = df.sort_values('Number of Likes', ascending=False)
        first_post_url = df5.iloc[0]['Post URL']

        st.divider()
        st.title("AI Insights")
        assistant_response = f"Most Liked Post: {first_post_url}, Which Has {df5.iloc[0]['Number of Likes']} Likes and {df5.iloc[0]['Number of Reposts']} Reposts on it."
        st.write(assistant_response)
        st.divider()

    else:
        st.write(f"Request failed with status code {api_res.status_code}")

def main():
    st.set_page_config(page_title="LinkedIn Sentiment Analysis", layout="wide")
    purl = st.text_input("Enter Your LinkedIn Profile URL:")

    if st.button("Extract Information"):
        scrapeposts()

if __name__ == "__main__":
    main()