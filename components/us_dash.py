
def get_current_total(metric) -> str:
    import requests
    import pandas as pd
    endpoint = 'https://covidtracking.com/api/v1/us/current.json'
    response = requests.get(endpoint)
    df = pd.DataFrame(response.json())
    pos = int(df[metric][0])
    return pos