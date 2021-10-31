import re
import pandas as pd
import datetime


def preprocess(data):
    # Pattern for separating messages and dates
    # Create pattern for 29/07/2020, 8:12 pm - and then split with this pattern
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[ap]m\s-\s'

    # Get the messages in a separate list by breaking string using pattern
    messages = re.split(pattern, data)[1:]
    # Get all dates by matching pattern because pattern is for dates
    dates = re.findall(pattern, data)

    dates2 = []

    for date in dates:
        first = date[0:12]
        middle = date[12:len(date)-3]
        middle = str(datetime.datetime.strptime(middle, '%I:%M %p'))
        middle = middle[11:len(middle)-3]
        last = ' - '
        dates2.append(first+middle+last)

    # Create DataFrame
    # df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df = pd.DataFrame({'user_message': messages, 'message_date': dates2})
    # convert message_date type
    # df['message_date'] = pd.to_datetime(
    #     df['message_date'], format='%d/%m/%Y, %H:%M %p - ')
    df['message_date'] = pd.to_datetime(
        df['message_date'], format='%d/%m/%Y, %H:%M - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)
    df.dropna(inplace=True)

    # Separate users and messages by separating from : and if there is no : means it is a group notification
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Separate all date parts
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
