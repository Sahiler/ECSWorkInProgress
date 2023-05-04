from random import randrange # from prefect.client.orion import create_flow
import requests
import pandas as pd
import io
import json
from prefect.artifacts import create_table_artifact
from prefect import task, flow, get_run_logger

    
@flow(name = "Create country artifact")
def pull_api_content(url: str): 
    r = requests.get(url).text
    df = pd.read_json(io.StringIO(r))
       
    create_table_artifact(
            key = "country-dataframe",
            table = df.to_dict('list'),
            description = "# Data frame of the countries in the world"
        )
    
    return df

@flow(name = "Create island artifact")
def find_islands(df):
    df_islands = df[df["borders"].isnull()]
    ret = df_islands.to_dict('list')
    create_table_artifact(
            key="island-dataframe",
            table=ret,
            description= "# Data frame of the country - islands in the world"
        )
    
    return df_islands

if __name__ == "__main__":
    url = r'https://restcountries.com/v3.1/all'
    df = pull_api_content(url)
    found_islands = find_islands(df)






