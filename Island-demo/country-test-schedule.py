import requests
import pandas as pd
import io

    
def pull_api_content(url: str): 
    r = requests.get(url).text
    df = pd.read_json(io.StringIO(r))
    print(f"Created country table : {df}")
    return df

def find_islands(df):
    df_islands = df[df["borders"].isnull()]
    print(f"Created island table: {df_islands}")
    return df_islands

if __name__ == "__main__":
    url = r'https://restcountries.com/v3.1/all'
    df = pull_api_content(url)
    found_islands = find_islands(df)


