import pandas as pd
import re


def filter_by_date(df, start_date, end_date):
    return df[(df['date'] >= start_date) & (df['date'] <= end_date)]


def preprocessor(data):
    pattern = r"\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2}\s?[AP]M - "

    messages = re.split(pattern, data)[1:]
    date = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'date': date})
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y, %I:%M %p - ')

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['month_name'] = df['date'].dt.month_name()
    df['week_of_month'] = (df['date'].dt.day - 1) // 7 + 1
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour

    df['hour_range'] = df['hour'].apply(lambda x: f"{x:02d}-{(x+1) % 24:02d}")

    user = []
    message = []
    pattern = r'^(.*?): (.*)$'

    for msg in df['user_message']:
        entry = re.split(pattern, msg)
        if entry[1:]:
            user.append(entry[1])
            message.append(entry[2])
        else:
            user.append("group_notification")
            message.append(entry[0])

    df['user'] = user
    df['message'] = message

    df = df.drop('user_message', axis=1)

    return df
