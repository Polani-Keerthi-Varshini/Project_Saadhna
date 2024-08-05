import streamlit as st
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from newspaper import Article
import nltk
nltk.download('punkt')
st.set_page_config(page_title='Instant Insight: Real-Time News Summarizer')
DEFAULT_NEWS_COUNT = 20
def fetch_news_search_topic(topic):
    site = 'https://news.google.com/rss/search?q={}'.format(topic)
    op = urlopen(site)
    rd = op.read()  
    op.close() 
    sp_page = soup(rd, 'xml')  
    news_list = sp_page.find_all('item')  
    return news_list
def fetch_top_news():
    site = 'https://news.google.com/news/rss'
    op = urlopen(site)  
    rd = op.read()  
    op.close()  
    sp_page = soup(rd, 'xml')  
    news_list = sp_page.find_all('item')  
    return news_list
def fetch_category_news(topic):
    site = 'https://news.google.com/news/rss/headlines/section/topic/{}'.format(topic)
    op = urlopen(site)  
    rd = op.read()  
    op.close()  
    sp_page = soup(rd, 'xml')  
    news_list = sp_page.find_all('item')  
    return news_list
def display_news(list_of_news, news_quantity=DEFAULT_NEWS_COUNT):
    for c, news in enumerate(list_of_news[:news_quantity], 1):
        st.write('**({}) {}**'.format(c, news.title.text))
        news_data = Article(news.link.text)
        try:
            news_data.download()
            news_data.parse()
            news_data.nlp()
        except Exception as e:
            st.error(e)
        with st.expander(news.title.text):
            st.markdown(
                '''<h6 style='text-align: justify;'>{}"</h6>'''.format(news_data.summary),
                unsafe_allow_html=True)
            st.markdown("[Read more at {}...]({})".format(news.source.text, news.link.text))
        st.success("Published Date: " + news.pubDate.text)
def run():
    st.title("Instant Insight: Real-Time News Summarizer")    
    category = ['--Select--', 'Trending News', 'All Topics', 'Search🔍']
    cat_op = st.selectbox('Select your Category', category)
    if cat_op == category[0]:
        st.warning('Please select Type!!')
    elif cat_op == category[1]:
        st.subheader("Here is the Trending news for you")
        news_list = fetch_top_news()
        display_news(news_list)
    elif cat_op == category[2]:
        av_topics = ['Choose Topic', 'WORLD', 'NATION', 'BUSINESS', 'TECHNOLOGY', 'ENTERTAINMENT', 'SPORTS', 'SCIENCE',
                     'HEALTH']
        st.subheader("Choose Any Topic")
        chosen_topic = st.selectbox("Choose your Topic here", av_topics)
        if chosen_topic == av_topics[0]:
            st.warning("Please Choose the Topic")
        else:
            news_list = fetch_category_news(chosen_topic)
            if news_list:
                st.subheader("Here are the some {} News for you".format(chosen_topic))
                display_news(news_list)
            else:
                st.error("No News found for {}".format(chosen_topic))
    elif cat_op == category[3]:
        user_topic = st.text_input("Enter your Topic🔍")
        if st.button("Search") and user_topic != '':
            user_topic_pr = user_topic.replace(' ', '')
            news_list = fetch_news_search_topic(topic=user_topic_pr)
            if news_list:
                st.subheader("Here are the some {} News for you".format(user_topic.capitalize()))
                display_news(news_list)
            else:
                st.error("No News found for {}".format(user_topic))
        else:
            st.warning("Please write Topic Name to Search🔍")
run()