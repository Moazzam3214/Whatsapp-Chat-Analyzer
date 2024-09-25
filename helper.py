from urlextract import URLExtract
from wordcloud import WordCloud
import emoji
from collections import Counter
import pandas as pd
from pandas.api.types import CategoricalDtype
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
import seaborn as sns
import streamlit as st


def display_bar_plot(title, data, x_label, y_label, palette):
    st.markdown(f"### {title}")
    fig, ax = plt.subplots()
    sns.barplot(x=data.index, y=data.values, palette=palette, ax=ax)
    for i, v in enumerate(data.values):
        ax.text(i, v, str(v), ha='center', va='bottom')
    plt.xticks(rotation='vertical')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    st.pyplot(fig)


def display_line_plot(x, y, title, x_label, y_label, color='red'):
    fig, ax = plt.subplots()

    ax.plot(x, y, color=color)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    ax.xaxis.set_major_locator(MaxNLocator(nbins=20))

    plt.xticks(rotation=45, ha='right')

    # Optionally format dates if 'x' contains dates
    if pd.api.types.is_datetime64_any_dtype(x):
        ax.xaxis.set_major_formatter(mdates.DateFormatter(
            '%Y-%m-%d'))

    plt.tight_layout()
    st.pyplot(fig)


def display_heatmap(data, title, x_label, y_label):
    fig, ax = plt.subplots(figsize=(20, 6))
    sns.heatmap(data, annot=True, fmt='d', ax=ax)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    st.pyplot(fig)


def fetch_stats(df):
    num_messages = df.shape[0]
    num_words = df['message'].apply(lambda x: len(x.split())).sum()
    num_media = df[df['message'] == '<Media omitted>'].shape[0]
    extractor = URLExtract()
    num_links = df['message'].apply(
        lambda x: len(extractor.find_urls(x))).sum()
    return num_messages, num_words, num_media, num_links


def fetch_most_busy_day(df):
    x = df['day_name'].value_counts()
    return x


def fetch_most_busy_month(df):
    x = df['month_name'].value_counts().head(5)
    return x


def fetch_most_busy_user(df):
    x = df['user'].value_counts().head(10)
    df = round((x / df.shape[0]) * 100,
               2).reset_index().rename(columns={'user': 'Name', 'count': 'Percentage'})
    return x, df


def fetch_wordcloud(df):
    # Remove the filtering here
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>']

    with open('stop_hinglish.txt', 'r') as file:
        stop_words = file.read()

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    temp['message'] = temp['message'].apply(remove_stop_words)

    wc = WordCloud(width=500, height=500, min_font_size=10,
                   background_color='white')
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def fetch_emojis(df):
    # Remove the filtering here
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(
        10), columns=['Emoji', 'Count'])
    return emoji_df


def fetch_monthly_timeline(df):
    # Remove the filtering here
    monthly_timeline_df = df.groupby(['year', 'month', 'month_name']).count()[
        'message'].reset_index()
    monthly_timeline_df['time'] = monthly_timeline_df['month_name'].astype(
        str) + '-' + monthly_timeline_df['year'].astype(str)
    return monthly_timeline_df


def fetch_weekly_timeline(df):
    # Remove the filtering here
    weekly_timeline_df = df.groupby(['year', 'month_name', 'week_of_month'])[
        'message'].count().reset_index()
    weekly_timeline_df['year_month_week'] = weekly_timeline_df['year'].astype(
        str) + '-' + weekly_timeline_df['month_name'].astype(str) + '-' + weekly_timeline_df['week_of_month'].astype(str)
    return weekly_timeline_df


def fetch_daily_timeline(df):
    # Remove the filtering here
    daily_timeline_df = df.groupby(['year', 'month_name', 'day']).count()[
        'message'].reset_index()
    daily_timeline_df['year_month_day'] = daily_timeline_df['year'].astype(
        str) + '-' + daily_timeline_df['month_name'].astype(str) + '-' + daily_timeline_df['day'].astype(str)
    return daily_timeline_df


def fetch_activity_map(selected_user, df):
    # Remove the filtering here
    activity_map_df = df.groupby(['year', 'month_name', 'day']).count()[
        'message'].reset_index()
    return activity_map_df


def fetch_hourly_activity_of_day(df):
    # Remove the filtering here
    hour_order = [f"{hour:02d}-{(hour+1) % 24:02d}" for hour in range(24)]
    hour_cat_type = CategoricalDtype(categories=hour_order, ordered=True)

    df['hour_range'] = df['hour_range'].astype(hour_cat_type)

    hourly_activity_of_day_pivot_table = df.pivot_table(
        index='day_name',
        columns='hour_range',
        values='message',
        aggfunc='count'
    ).fillna(0)

    return hourly_activity_of_day_pivot_table
