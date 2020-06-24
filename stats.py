import pandas as pd

def get_data(endpoint: str) -> pd.DataFrame:
    """
    get_data
    :desc api helper function
    :param endpoint: str
    :return pd.DataFrame:
    """
    import requests
    import pandas as pd

    response = requests.get(endpoint)
    df = pd.DataFrame(response.json())
    return df.sort_values(by=['date'])


def format_dates(list_col) -> list:
    # Convert yyyymmdd to date for axis
    from datetime import datetime
    new_list = []
    for i in list_col:
        date_object = datetime.strptime(str(i), '%Y%m%d')
        new_list.append(date_object.strftime('%Y-%m-%d'))
    return new_list


def get_states() -> list:
    """Get the list of US States"""
    df = get_data('https://covidtracking.com/api/v1/states/current.json')
    return df['state'].tolist()


def get_positive() -> list:
    """get the positive rate in a list"""
    df = get_data('https://covidtracking.com/api/v1/states/current.json')
    return df['positive'].tolist()


def get_us_hist() -> pd.DataFrame:
    """Hit the historical US endpoint"""
    df = get_data('https://covidtracking.com/api/v1/us/daily.json')
    return df

def get_us_hist_dates():
    """Get dates for us hist x axis"""
    df = get_data('https://covidtracking.com/api/v1/us/daily.json')
    return df['date']


def get_us_hist_positive():
    """get column of positive from us daily data"""
    df = get_data('https://covidtracking.com/api/v1/us/daily.json')
    return df['positive']


def get_states_hist(state: str) -> pd.DataFrame:
    """Pass in the date: str to get historical states data"""
    endpoint = 'https://covidtracking.com/api/v1/states/' + state.lower() + '/daily.json'
    df = get_data(endpoint)
    return df


def get_new_metrics(df: pd.DataFrame, measure: str) -> list:
    # calculate new cases and deaths
    """
        takes in pd.DataFrame and column name: str,
        returns difference from previous day
    """
    new_df = df[measure].diff(periods=1)
    return new_df.tolist()


def moving_average(col_list: list) -> list:
    '''input list, get the 7 day moving average'''
    import pandas as pd
    week = 7
    col_series = pd.Series(col_list)
    windows = col_series.rolling(week)
    return windows.mean().tolist()


def get_population_data() -> pd.DataFrame:
    '''read the csv of population data and get pd.DataFrame'''
    import os
    import pandas as pd
    dirname = os.path.dirname(__file__)
    file = os.path.join(dirname, "assets/data/populationdata.csv")
    return pd.read_csv(file)
