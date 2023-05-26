def holidayEntity(holiday) -> dict:
    return {
        "id": str(holiday["_id"]),
        "name": holiday["name"],
        "date": holiday["date"],
        "created_at": holiday["created_at"],
        "updated_at": holiday["updated_at"]
    }


def holidayResponseEntity(holiday) -> dict:
    return {
        "id": str(holiday["_id"]),
        "name": holiday["name"],
        "date": holiday["date"],
        "created_at": holiday["created_at"],
        "updated_at": holiday["updated_at"]
    }


def embeddedHolidayResponse(holiday) -> dict:
    return {
        "id": str(holiday["_id"]),
        "name": holiday["name"],
        "date": holiday["date"],
    }

def holidayListEntity(holidays) -> list:
    return [holidayEntity(holiday) for holiday in holidays]