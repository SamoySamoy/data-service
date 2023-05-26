from datetime import datetime
from fastapi import Depends, HTTPException, status, APIRouter, Response
from pymongo.collection import ReturnDocument
from app import schemas
from app.database import Holiday
from app.jwt import require_user
from app.serializers.holidaySerializers import holidayEntity, holidayListEntity
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError

router = APIRouter()

# get all holidays
@router.get('/')
def get_holidays(limit: int = 10, page: int = 1, search: str = '', user_id: str = Depends(require_user)):
    skip = (page - 1) * limit
    pipeline = [
        {'$match': {}},
        {'$lookup': {'from': 'users', 'localField': 'user',
                     'foreignField': '_id', 'as': 'user'}},
        {'$unwind': '$user'},
        {
            '$skip': skip
        }, {
            '$limit': limit
        }
    ]
    holidays = holidayListEntity(Holiday.aggregate(pipeline))
    return {'status': 'success', 'results': len(holidays), 'holidays': holidays}

# create holiday
@router.post('/', status_code=status.HTTP_201_CREATED)
def create_holiday(holiday: schemas.HolidayBaseSchema, user_id: str = Depends(require_user)):
    holiday.created_at = datetime.utcnow()
    holiday.updated_at = holiday.created_at
    try:
        result = Holiday.insert_one(holiday.dict())
        pipeline = [
            {'$match': {'_id': result.inserted_id}},
            {'$lookup': {'from': 'users', 'localField': 'user',
                         'foreignField': '_id', 'as': 'user'}},
            {'$unwind': '$user'},
        ]
        new_holiday = holidayListEntity(Holiday.aggregate(pipeline))[0]
        return new_holiday
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Holiday with date: '{holiday.date}' already exists")


""" @router.put('/{id}')
def update_post(id: str, payload: schemas.UpdatePostSchema, user_id: str = Depends(require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")
    updated_post = Post.find_one_and_update(
        {'_id': ObjectId(id)}, {'$set': payload.dict(exclude_none=True)}, return_document=ReturnDocument.AFTER)
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post with this id: {id} found')
    return postEntity(updated_post)


@router.get('/{id}')
def get_post(id: str, user_id: str = Depends(require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")
    pipeline = [
        {'$match': {'_id': ObjectId(id)}},
        {'$lookup': {'from': 'users', 'localField': 'user',
                     'foreignField': '_id', 'as': 'user'}},
        {'$unwind': '$user'},
    ]
    db_cursor = Post.aggregate(pipeline)
    results = list(db_cursor)

    if len(results) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post with this id: {id} found")

    post = postListEntity(results)[0]
    return post


@router.delete('/{id}')
def delete_post(id: str, user_id: str = Depends(require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")
    post = Post.find_one_and_delete({'_id': ObjectId(id)})
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post with this id: {id} found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)

 """