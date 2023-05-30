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
from app.crawl import (
    get_stock_company_profile,
    get_stock_shareholders,
    get_stock_prices,
)
from app.celery import celery_app


router = APIRouter()


# user get specific stock data
@router.get("/{stock}")
def get_stock(stock: str):
    pipeline = [
        {"$match": {"name": stock}},
    ]
    db_cursor = Stock.aggregate(pipeline)
    results = list(db_cursor)

    if len(results) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No stock with this name: {stock} found",
        )

    result = stockListEntity(results)[0]
    return result


# create/update stock data (crawl from iboard)
@router.post("/{stock}")
async def crawl_stock(stock: str, payload: schemas.StockCrawlSchema):
    payload.name = stock
    payload.company_info = get_stock_company_profile.delay(stock).get()
    payload.shareholders = get_stock_shareholders.delay(stock).get()
    payload.prices = get_stock_prices.delay(stock).get()
    payload.created_at = datetime.utcnow()
    payload.updated_at = payload.created_at
    try:
        result = Stock.insert_one(payload.dict())
        pipeline = [
            {"$match": {"_id": result.inserted_id}},
        ]
        result = stockListEntity(Stock.aggregate(pipeline))[0]
        return result
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Stock with code: '{payload.name}' already exists",
        )

# delete all database:
@router.delete("/all")
def delete_all():
    result = Stock.delete_many({})
    return ("Delete all success")


