def stockEntity(stock) -> dict:
    return {
        "id": str(stock["_id"]),
        "name": stock["name"],
        "company_info": stock["company_info"],
        "shareholders": stock["shareholders"],
        "prices": stock["prices"],
        "created_at": stock["created_at"],
        "updated_at": stock["updated_at"]
    }


def stockListEntity(stocks) -> list:
    return [stockEntity(stock) for stock in stocks]