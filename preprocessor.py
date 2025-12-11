import re
import pandas as pd
import datetime


def preprocess(data):
    # Pattern for separating messages and dates
    # Matches: 10/13/24, 1:33 PM - 
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APap][Mm]\s-\s'

    # Get the messages in a separate list by breaking string using pattern
    messages = re.split(pattern, data)[1:]
    # Get all dates by matching pattern because pattern is for dates
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    
    # Clean the date string by removing the trailing ' - '
    df['message_date'] = df['message_date'].str.replace(' - ', '', regex=False)
    # unexpected narrow no-break space character is sometimes present
    df['message_date'] = df['message_date'].str.replace('\u202f', ' ', regex=False)
    
    # Convert message_date type
    # handles 2 digit year (%y) and AM/PM (%p)
    # Format: 10/13/24, 1:33 PM
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p') 
    
    # NOTE: The user provided snippet has a narrow no-break space (U+202F) between time and AM/PM sometimes?
    # Actually, looking at the user request: "1:33 PM". It's a standard space or U+202F.
    # Chrome/Android exports often use U+202F.
    # Let's handle generic whitespace in format?
    # pd.to_datetime format string is strict. 
    # Let's normalize the string first.
    
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
