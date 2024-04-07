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
import os
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
    #with open('demo.json') as f:
        json_data =  json.loads(api_res.text)#json.load(f)
        data = json_data['data'][:10]  # Limit to first 10 post URLs

        post_urls = [item['post_url'] for item in data]
        num_likes = [item['num_likes'] for item in data]
        num_comments = [item['num_comments'] for item in data]
        num_reposts = [item['num_reposts'] for item in data]
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
        # 'Number of Appreciations': num_appreciations,
        'Number of Reposts': num_reposts,
        })

        df1 = pd.DataFrame({
        'Number of Likes': num_likes,
        })
        
        df2 = pd.DataFrame({
        'Number of Comments': num_comments,
        })
        
        df3 = pd.DataFrame({
        # 'Number of Appreciations': num_appreciations,
        })
        
        df4 = pd.DataFrame({
        'Number of Reposts': num_reposts,
        })


        
        part1,part2 = st.columns(2)
        with part1:
            st.bar_chart(data = df1, y = "Number of Likes")
        with part2:
            st.bar_chart(data = df2, y = "Number of Comments")
        part3,part4 = st.columns(2)
        # with part3:
            # st.line_chart(df3, y = "Number of Appreciations")
        with part4:
            st.line_chart(df4, y = "Number of Reposts")
        st.title("Last 10 Posts:")
        st.table(df)
        df5 = df.sort_values('Number of Likes', ascending=False)
        first_post_url = df5.iloc[0]['Post URL']
        st.divider()
        st.title("AI Insights")
        assistant_response = f"Most Liked Post: {first_post_url}, Which Has {df5.iloc[0]['Number of Likes']} Likes and {df5.iloc[0]['Number of Reposts']} Reposts on it."
        with st.chat_message("assistant"):
                st.markdown(assistant_response)
        st.divider()
        #post_id = first_post_url.split(':')[-1].strip('/')
        st.title("Recently Most Liked Posts:")
        st.table(df5)
        #st.write(post_id)
        chart_data = pd.DataFrame(
        {
            # "Number of Appreciations": num_appreciations,
            "Number of Likes": num_likes,
            "Number of Reposts": num_reposts,
        })
        st.area_chart(chart_data, y=["Number of Likes","Number of Reposts"])
    #else:
    #    st.write("ERROR 404")
                 
    #else:
    #    st.write(f"Request failed with status code {api_res.status_code}")
        
with st.sidebar:
    choose = option_menu("DASHBOARD", ["My Info","Post Analyzer","Competitor Analysis"],
                         icons=['linkedin', 'file-post', 'kanban', 'book','person lines fill'],
                         menu_icon="list", default_index=0,
                         styles={
        "container": {"padding": "5!important",},
        "icon": {"color": "#000", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#0087FF"},
        "nav-link-selected": {"background-color": "#0087FF"},
    }
    )

placeholder = st.empty()


if choose == "My Info":
    st.title("LinkedIn Analytics")
    components.html("""  <script type="text/javascript" src="https://ssl.gstatic.com/trends_nrtr/3523_RC02/embed_loader.js"></script>
  <script type="text/javascript">
    trends.embed.renderWidget("dailytrends", "", {"geo":"IN","guestPath":"https://trends.google.com:443/trends/embed/"});
  </script>
""")
    purl = st.text_input("Enter Your LinkedIn Profile URL:")
    if st.button("Extract Information"):
        scrapeposts()

elif choose == "Post Analyzer":
    st.title('📱 LinkedIn Posts Scanner ')
    api_key = "8f5ea1db-f14f-4528-a885-c7cf8661227a"
    url = "https://api.oneai.com/api/v0/pipeline"
    headers = {
      "api-key": api_key, 
      "content-type": "application/json"
    }
    input_url = st.text_input('Drop the LinkedIn post link here 👇')
    payload = {
            "input": input_url,
            "input_type": "article",
            "output_type": "json",
            "steps": [
                {
                "skill": "html-extract-article"
                }
            ],
        }
    req1 = requests.post(url, json=payload, headers=headers)
    article_data = req1.json()
    print(req1.json)
    if st.button("Extract Information"):
        article_text = article_data['output'][0]['contents'][0]['utterance']
        st.text("FETCHED ALL THE COMMENTS!")
        st.text("FEEDING ALL COMMENTS TO AI...")
        api_base = "https://api.endpoints.anyscale.com/v1/chat/completions"
        token = "esecret_x87vhql3nwigeupf8exw4egzw5" #esecret_x87vhql3nwigeupf8exw4egzw5
        url = api_base
        body = {
                "model": "meta-llama/Llama-2-70b-chat-hf",
                "messages": [{"role": "system", "content": "You are an helpful assistant"}, 
                {"role": "user", "content": f"{article_text} above are the comments of  linkedin post, take first few comments,mention the users  and give meaningfull sentiment analysis and insights of  comments along with the conclusion based on the comments in a way that is apealing for me to read with bullet points ,start directly with the answer , dont say Sure, heres my analysis of the first few comments on Gary Vaynerchuks LinkedIn post"}],
                "temperature": 0.7
                }
        res1 =  requests.post(url, headers={"Authorization": f"Bearer {token}"}, json=body)
        data = res1.json()
        assistant_response = data["choices"][0]["message"]["content"]
        message_placeholder = st.empty()
        full_response = ""
        with st.chat_message("assistant"):
                st.markdown(assistant_response)
        



if choose == "Competitor Analysis":
    username = st.text_input("Enter Your Username:")
    password = st.text_input("Enter Your Password:",type="password")
    comp_un = st.text_input("Enter Your Competitor's Profile Username:")
    if st.button("Extract Information"):
        Options = Options()
        Options.headless = True
        furl = f'https://www.linkedin.com/in/{comp_un}?original_referer=https://google.com'
        url = comp_un
        driver = webdriver.Firefox()
        driver.get('https://www.linkedin.com/login')
        driver.implicitly_wait(4)
        username_input = driver.find_element(By.XPATH,'//*[@id="username"]')
        username_input.send_keys(username)
        password_input = driver.find_element(By.XPATH,'//*[@id="password"]')
        password_input.send_keys(password)
        log_in_button = driver.find_element(By.XPATH,'/html/body/div/main/div[2]/div[1]/form/div[3]/button')
        log_in_button.click()
        driver.implicitly_wait(10)
        driver.get(url)
        driver.implicitly_wait(5)
        main_element = "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main"
        comment_elements = driver.find_elements(By.XPATH, '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[2]/span[1]')
        profile_elements = driver.find_elements(By.XPATH, '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[4]/div[3]/div/div/div/span[1]')# Adjust the class based on LinkedIn's structure
        #st.write(comment_elements)
        with open('output.txt', 'w') as f:
            for comment in comment_elements:
                comment_text = comment.text.strip()
                comment_text = re.sub(r'\[[\s\S]*?\]', '', comment_text)
                f.write(comment_text + '\n')
        with open('output.txt', 'w') as f:
            for profile in profile_elements:
                profile_text = profile.text.strip()
                profile_text = re.sub(r'\[[\s\S]*?\]', '', profile_text)
                f.write(profile_text + main_element+ '\n')
        driver.implicitly_wait(4)
        driver.quit()
        with open('output.txt', 'r') as f:
            content = f.read()
        st.text("FETCHED ALL THE COMMENTS!")
        st.text("FEEDING ALL COMMENTS TO AI...")
        api_base = "https://api.endpoints.anyscale.com/v1/chat/completions"
        token = "esecret_ase3ntamfk5ayicf5qx5bw2fpr"
        url = api_base
        body = {
                "model": "meta-llama/Llama-2-70b-chat-hf",
                "messages": [{"role": "system", "content":furl}, 
                {"role": "user", "content": f"using below data of my linkedin competitor, give me usefull insights: {content}"}],
                "temperature": 0.7
                }
        res1 =  requests.post(url, headers={"Authorization": f"Bearer {token}"}, json=body)
        data = res1.json()
        if "choices" in data and data["choices"]:
            if "message" in data["choices"][0] and "content" in data["choices"][0]["message"]:
                assistant_response = data["choices"][0]["message"]["content"]
            else:
                print("Error: 'message' key or 'content' key not found in the first item of the 'choices' list.")
        else:
            print("Error: 'choices' key not found in the data dictionary or the 'choices' list is empty.")

        message_placeholder = st.empty()
        full_response = ""
        with st.chat_message("assistant"):
                st.markdown(assistant_response)
        
st.write("©LostGeeks") 
#MainMenu {visibility: hidden;}
st.markdown("""
    <style>
            footer {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}

    </style>
""", unsafe_allow_html=True)
