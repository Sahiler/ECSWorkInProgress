from prefect import flow, task, get_run_logger
from prefect_aws import AwsCredentials
from prefect_aws.ecs import ECSTask
import requests
import pandas as pd
import io
import json
from prefect import task, flow, get_run_logger
from prefect.artifacts import create_table_artifact
from prefect.blocks.system import Secret

from prefect_aws import AwsCredentials
from prefect.blocks.system import Secret

# secret_block = Secret.load("aws-secret")

# AwsCredentials(
#     aws_access_key_id="ASIAWUBGH2JR3ZZBGMFJ",
#     aws_secret_access_key=secret_block.get(),
#     aws_session_token="IQoJb3JpZ2luX2VjEJr//////////wEaCXVzLWVhc3QtMiJHMEUCIQD1cAZIqmKAYkFNuW5cfKTrygyPigjbrwMWrNHbO8304wIgTiJeJZ9sROuA20p4/7Jdlod4CASviinOaUy2s/mZNikqhwMIk///////////ARAAGgw0NTUzNDY3Mzc3NjMiDAGH1QbmtgBRH1cZ1CrbAuBVwl7Ws2tTbiz7izNck83KhSyZUtgrL3ohEvcrr1ukKbApwmAzxQwUXmtU1Wh/ZWiKgqVf8QiYQmR/Bsp8Dj6H/GDBK7/m3tR4owzOGlgVpjBfWBQTfdc2vj32Z0+h6JqlMmAfaP82lEQncuLpXHrWjnG/1yV6ZRGSCpsLpZ4X91T3sFQPavKpFi0U7mtdVSAcdSboWjYMRjYBHB9Ug7V5HfwzALycNxrBTtAaPyMjBkAWXWWlESELg9nXmccedOXyw5PMiQvma3uK2LTYUAOk4NyNiz6WUBSn6qWTFWNOoFmdZggplL78lAanBLKcEtvfqM+XFQmhDmW1wiY4t3zs+OMa/258V4Qr3JQNVsDYl5mLY04enO2xAIQR4nBI1LAJ4Q8EPGBWemxOjDAVwPfxEkNJYjMRUDQfTBII75aZqTZXeTs5NIid3haz3EY2IWw/hmuyRnPSXJtnMNT6haIGOqcBoPoUXqfT8xn0IOk8uCv2dhmVS7SnJWhKZcmVQ73wRH5JAIcL0oyUSDdOVIvnlgdrzyjwJ8VeBkZnKLcwH07OXtPcKZ4my44joaFDDMe0SzTQngQDpi9y32OZtZKdWJ9BxoSf1x40TmqQdZehjyk0tydPdV3eLbrpozIyis4s0fz6H6GQbUUx1RKGXRlFFvPdHYGoyl7EV35vJ/y2VVEBY2A3gShWk7c=",  # replace this with token if necessary
#     region_name="us-east-2"
# ).save("creds-power-user")


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
    found_islands = find_islands()