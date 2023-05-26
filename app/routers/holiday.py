from datetime import datetime, date, timedelta
import calendar 
from fastapi import Depends, HTTPException, status, APIRouter, Response
from pymongo.collection import ReturnDocument
from app import schemas
from app.database import Holiday
from app.jwt import require_user
from app.serializers.holidaySerializers import holidayEntity, holidayListEntity, listEntity
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError
from app.utils import format_date

router = APIRouter()


# get all holidays
@router.get("/")
def get_holidays(
    search: str = "",
    user_id: str = Depends(require_user),
):  
    
    pipeline = [{"$match": {}},]
    holidays = holidayListEntity(Holiday.aggregate(pipeline))
    
    return {"status": "success", "results": len(holidays), "holidays": holidays}

#get all holidays plus weekend data
@router.get("/all")
def get_all(
    user_id: str = Depends(require_user)
):
    pipeline = [{"$match": {}},]
    holidays = listEntity(Holiday.aggregate(pipeline))
    
    # Get all Saturdays and Sundays of the current year until today
    current_year = date.today().year
    today = date.today()
    all_weekends = []
    for month in range(1, today.month + 1):
        for day in calendar.monthcalendar(current_year, month):
            if day[calendar.SATURDAY] != 0:
                weekend_date = date(current_year, month, day[calendar.SATURDAY])
                if weekend_date <= today:
                    all_weekends.append(weekend_date)
            if day[calendar.SUNDAY] != 0:
                weekend_date = date(current_year, month, day[calendar.SUNDAY])
                if weekend_date <= today:
                    all_weekends.append(weekend_date)
    all_weekends = list(map(format_date, all_weekends)) 
    # Combine holidays and weekends
    all_dates = holidays + all_weekends
    
    return {"status": "success", "results": len(all_dates), "all": all_dates}
# create holiday
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_holiday(
    payload: schemas.HolidayBaseSchema, user_id: str = Depends(require_user)
):
    payload.created_at = datetime.utcnow()
    payload.updated_at = payload.created_at
    try:
        result = Holiday.insert_one(payload.dict())
        pipeline = [
            {"$match": {"_id": result.inserted_id}},
        ]
        new_holiday = holidayListEntity(Holiday.aggregate(pipeline))[0]
        return new_holiday
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Holiday with date: '{payload.date}' already exists",
        )


# update specific holiday
@router.put("/{id}")
def update_holiday(
    id: str, payload: schemas.HolidayBaseSchema, user_id: str = Depends(require_user)
):
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid id: {id}"
        )
    updated_holiday = Holiday.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": payload.dict(exclude_none=True)},
        return_document=ReturnDocument.AFTER,
    )
    if not updated_holiday:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No post with this id: {id} found",
        )
    return holidayEntity(updated_holiday)


# get specific holiday
@router.get("/{id}")
def get_holiday(id: str, user_id: str = Depends(require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid id: {id}"
        )
    pipeline = [
        {"$match": {"_id": ObjectId(id)}},
    ]
    db_cursor = Holiday.aggregate(pipeline)
    results = list(db_cursor)

    if len(results) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No holiday with this id: {id} found",
        )

    holiday = holidayListEntity(results)[0]
    return holiday

# delete all database:
@router.delete("/all")
def delete_all(user_id: str = Depends(require_user)):
    result = Holiday.delete_many({})
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# delete specific holiday
@router.delete("/{id}")
def delete_holiday(id: str, user_id: str = Depends(require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid id: {id}"
        )
    holiday = Holiday.find_one_and_delete({"_id": ObjectId(id)})
    if not holiday:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No holiday with this id: {id} found",
        )
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)


