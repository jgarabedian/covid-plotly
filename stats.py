def get_data(endpoint):
    import requests
    import pandas as pd

    response = requests.get(endpoint)
    df = pd.DataFrame(response.json())
    return df.sort_values(by=['date', 'state'])


def get_states():
    df = get_data('https://covidtracking.com/api/v1/states/current.json')
    return df['state'].tolist()


def get_positive():
    df = get_data('https://covidtracking.com/api/v1/states/current.json')
    return df['positive'].tolist()


def get_us_hist_dates():
    df = get_data('https://covidtracking.com/api/v1/us/daily.json')
    return df['date']


def get_us_hist_positive():
    df = get_data('https://covidtracking.com/api/v1/us/daily.json')
    return df['positive']


def get_states_hist(state):
    endpoint = 'https://covidtracking.com/api/v1/states/' + state.lower() + '/daily.json'
    df = get_data(endpoint)
    return df


def get_new_metrics(df, measure):
    new_df = df[measure].diff(periods=1)
    return new_df.tolist()