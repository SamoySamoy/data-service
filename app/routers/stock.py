from datetime import datetime, date, timedelta
import calendar 
from fastapi import Depends, HTTPException, status, APIRouter, Response
from pymongo.collection import ReturnDocument
from app import schemas
from app.database import Stock
from app.jwt import require_user
from app.serializers.stockSerializers import stockEntity, stockListEntity
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError
from app.crawl import get_stock_company_profile, get_stock_shareholders, get_stock_prices

router = APIRouter()


# user get specific stock data
@router.get("/{stock}")
def get_stock(stock: str, user_id: str = Depends(require_user)):
    pipeline = [
        {"$match": {"name": stock}},
    ]
    db_cursor = Stock.aggregate(pipeline)
    results = list(db_cursor)

    if len(results) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No holiday with this id: {id} found",
        )

    result = stockListEntity(results)[0]
    return result

# create stock data (crawl from iboard)
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

