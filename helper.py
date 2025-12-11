from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extractor = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(df):
    df = df[df['user'] != 'group_notification']
    top_five_users = df['user'].value_counts().head()
    # Get the percentage of messages sent by each user
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return top_five_users, df


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # remove group notifications
    temp = df[df['user'] != 'group_notification']
    # remove media omitted messages
    temp = temp[temp['message'] != '<Media omitted>\n']

    wc = WordCloud(width=500, height=500, min_font_size=10,
                   background_color='white')
    # remove stop words
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # remove group notifications
    temp = df[df['user'] != 'group_notification']
    # remove media omitted messages
    temp = temp[temp['message'] != '<Media omitted>\n']

    # remove stop words
    temp['message'] = temp['message'].apply(remove_stop_words)

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def get_emoji_data(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis_list = []
    for message in df['message']:
        emojis_list.extend(
            [c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(
        Counter(emojis_list).most_common(len(Counter(emojis_list))))

    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Create monthly timeline data frame
    monthly_timeline = df.groupby(['year', 'month_num', 'month']).count()[
        'message'].reset_index()

    time = []
    for i in range(monthly_timeline.shape[0]):
        time.append(monthly_timeline['month'][i] +
                    '-' + str(monthly_timeline['year'][i]))

    monthly_timeline['time'] = time

    return monthly_timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # Create daily timeline data frame
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline


def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()


def remove_stop_words(message):
    f = open('stop_mixenglish.txt', 'r')
    stop_words = f.read()
    words = []
    for word in message.lower().split():
        if word not in stop_words:
            words.append(word)
    return " ".join(words)


def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    user_heatmap = df.pivot_table(
        index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap
