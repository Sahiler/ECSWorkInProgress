import requests
import pandas as pd
import io
import json
from prefect import task, flow, get_run_logger
from prefect.artifacts import create_table_artifact
from prefect.blocks.system import Secret


# Access the stored secret
    
# replaced prints with log statements
@flow(name="Pull api data", retries = 1, retry_delay_seconds = 30)
def pull_api_content():
    secret_block = Secret.load("api-address")
    url = secret_block.get()

    r = requests.get(url).text
    df = pd.read_json(io.StringIO(r))
    logger = get_run_logger()
    logger.info(f"Created country table: {df}")

    return df

@flow(name="Extract islands", description = "Data table of island countries")
def find_islands():
    secret_block = Secret.load("api-address")
    url = secret_block.get()

    r = requests.get(url).text
    df = pd.read_json(io.StringIO(r))    
    df_islands = df[df["borders"].isnull()]
    logger = get_run_logger()
    logger.info(f"Created island table: {df_islands}")

    return df_islands


if __name__ == "__main__":
    # url = r'https://restcountries.com/v3.1/all'
    df = pull_api_content()
    found_islands = find_islands()


