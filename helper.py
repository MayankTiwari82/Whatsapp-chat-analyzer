from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd


def fetch_stats(selected_user,df):
    if selected_user!='Overall':
        df=df[df['users']==selected_user]
    num_message = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())
    # fetching media message
    num_media_message = df[df['message'] == '<Media omitted>\n'].shape[0]

    #fetching the links media messages
    links = []
    extractor = URLExtract()
    for message in df['message']:
        links.extend(extractor.find_urls(message))
    k=len(links)



    return num_message, len(words), num_media_message,k,links


def fetch_links(selected_user,df):
    links = []
    extractor = URLExtract()
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return len(links)
def most_busy_user(df):
    x = df['users'].value_counts().head()
    df=round((df['users'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x,df
def create_wordcloud(selected_user,df):
    if selected_user!='Overall':
        df=df[df['users']==selected_user]
    temp = df[df['users'] != 'gropu_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)



    wc=WordCloud(width=500, height=500, min_font_size=10,background_color='white')
    temp['message']=temp['message'].apply(remove_stop_words)
    df_wc=wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc
def most_common_words(selected_user,df):

    if selected_user!='Overall':
        df=df[df['users']==selected_user]
    temp = df[df['users'] != 'gropu_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df=pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def monthly_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['users']==selected_user]

    timeline = df.groupby(['year', 'month_num', 'month_name']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month_name'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['users']==selected_user]
    daily_timeline = df.groupby('date_only').count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user!='Overall':
        df=df[df['users']==selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user!='Overall':
        df=df[df['users']==selected_user]

    return df['month_name'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user!='Overall':
        df=df[df['users']==selected_user]
    user_heatmap=df.pivot_table(index='day_name', columns='period', values='message',aggfunc='count').fillna(0)

    return user_heatmap