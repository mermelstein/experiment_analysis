from sqlalchemy import create_engine
import pandas as pd
import os


def engine(
    db_type="postgresql",
    user_name=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    host=os.environ.get("DB_HOST"),
    port=os.environ.get("DB_PORT"),
    db_name=os.environ.get("DB_NAME"),
):
    engine = create_engine(
        f"{db_type}://{user_name}:{password}@{host}:{port}/{db_name}"
    )
    return engine


def queryDB(query):
    df = pd.read_sql(query, con=engine())
    return df


def get_data(query):
    experiment_data = queryDB(query)
    return experiment_data
