from .db import Base
from sqlalchemy import Column ,Integer,String

class Store(Base):

    __tablename__ = 'stores'

    store_id: Column(String)
    timestamp_utc: Column(Integer)
    status: Column(String)

class BusinessHours(Base):

    __tablename__ = 'businesshours'

    store_id: Column(String)
    dayOfWeek: Column(Integer)
    start_time_local: Column(String)
    end_time_local: Column(String)

class Status(Base):

    __tablename__ = 'status'

    store_id: Column(String)
    timezone_str: Column(String)

class ReportData(Base):

    __tablename__ = 'reportdata'
    
    store_id: Column(Integer)
    uptime_last_hour: Column(Integer)
    uptime_last_day: Column(Integer)
    uptime_last_week: Column(Integer)
    downtime_last_hour: Column(Integer)
    downtime_last_day: Column(Integer)
    downtime_last_week: Column(Integer)
