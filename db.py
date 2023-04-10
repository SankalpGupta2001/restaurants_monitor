import pymongo
import pandas as pd
import json
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import sessionmaker



SQLALCHEMY_DATABASE_URL = "mysql://root:@localhost/Res"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def insert_csv_data_to_db(file_path):
    df = pd.read_csv(file_path)
    df.to_sql('table_name', engine, if_exists='append', index=False)


def schedule_csv_data_insertion():
    scheduler = BackgroundScheduler()
    scheduler.add_job(insert_csv_data_to_db, 'interval', args=["store status(1).csv"], hours=1)
    scheduler.add_job(insert_csv_data_to_db, 'interval', args=["Menu hours.csv"], hours=1)
    scheduler.add_job(insert_csv_data_to_db, 'interval', args=["bq.results-20230125-202210-1674678181880.csv"], hours=1)
    scheduler.start()
    