from pydantic import BaseModel
class StoreSchema(Base):
    store_id: str
    timestamp_utc: datetime
    status: str

class BusinessHoursSchema(BaseModel):
    store_id: str
    dayOfWeek: int
    start_time_local: str
    end_time_local: str

class StatusSchema(BaseModel):
    store_id: str
    timezone_str: str

class ReportDataSchema(BaseModel):
    store_id: int
    uptime_last_hour: int
    uptime_last_day: float
    uptime_last_week: float
    downtime_last_hour: int
    downtime_last_day: float
    downtime_last_week: float
