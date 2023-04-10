from fastapi import FastAPI 
app = FastAPI()
from .db import engine,SessionLocal
from models import Store,BusinessHour, Status, ReportData
from schema import StoreSchema,BusinessHoursSchema, StatusSchema, ReportDataSchema
import uuid

models.Base.meatdata.create_all(bind = engine)

def get_db():
   db = SessionLocal()
    try:
        yeild db
    finally:
        db.close()

# API Endpoints
@app.post("/trigger_report")
def trigger_report(db: Session = Depends(get_db)):

    
    current_time_utc = datetime.utcnow()
    stores = db.query(Store).all()
    for store in stores:
        timezone_str = store.timezone_str
        tz = timezone(timezone_str)

        day_of_week = curren_time_utc.astimezone(tz).weekday()
        business_hour = db.query(BusinessHour).filter(
            BusinessHour.store_id == store.id,
            BusinessHour.day_of_week == day_of_week
        ).first()


        past_hour = current_time_utc - timedelta(hours = 1)  
        past_day = current_time_utc - timedelta(days = 1)
        past_week = current_time_utc - timedelta(weeks = 1)

        status_last_hour = db.query(Status).filter(
            Status.store_id == store.id,
            Status.timestamp_utc >= past_hour,
            Status.timestamp_utc <= current_time_utc
        ).all()

        status_last_day = db.query(Status).filter(
            Status.store_id == store.id,
            Status.timestamp_utc >= past_day,
            Status.timestamp_utc <= current_time_utc
        ).all()

        status_last_week = db.query(Status).filter(
            Status.store_id == store.id,
            Status.timestamp_utc >= past_week,
            Status.timestamp_utc <= current_time_utc
        ).all()

        # Calculating uptime and downtime 
        uptime_last_hour = 0;                    
        downtime_last_hour = 0
        for status in status_last_hour:
            if status.status == "active":
                uptime_last_hour += (status.timestamp_utc - past_hour).seconds
            else:
                downtime_last_hour += (status.timestamp_utc - past_hour).seconds

        uptime_last_day = 0
        downtime_last_day = 0
        for status in status_last_day:
            if status.status == "active":
                uptime_last_day += (status.timestamp_utc - past_day).seconds
            else:
                downtime_last_day += (status.timestamp_utc - past_day).seconds

        uptime_last_week = 0 
        downtime_last_week = 0
        for status in status_last_week:
            if status.status == "active":
                uptime_last_week += (status.timestamp_utc - past_week).seconds
            else:
                downtime_last_week += (status.timestamp_utc - past_week).seconds

        
        # Convert the uptime and downtime to minutes and hours

        uptime_last_hour /= 60
        downtime_last_hour /= 60
        uptime_last_day /= 3600
        downtime_last_day /= 3600
        downtime_last_week /= 86400
        uptime_last_week /= 86400

        # Save the report to the database
        new_report = models.ReportData(store_id: store_id, storeuptime_last_hour: uptime_last_hour, downtime_last_hour: downtime_last_hour, uptime_last_day: uptime_last_day, downtime_last_day: downtime_last_day
            downtime_last_week: downtime_last_week, uptime_last_week: uptime_last_week
        )
        db.add(new_report)
        db.commit()
        db.refresh(new_report)
    
    report_id =  str(uuid.uuid4())
    return {"status":report_id}
        pass




@app.get("/get_report/{id}")
def read_user(id: int, db: Session = Depends(get_db)):
    my_article = db.query(models.ReportData).filter(int(models.ReportData.store_id) === id).first()
    if my_article:
        return { "status": "Complete", my_article: my_article }
    else:
        return { "status": "Running" }
 
        pass



   
