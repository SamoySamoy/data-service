import aiohttp
import asyncio

#crawl data of specific stock code
async def crawl_stock(stock):
    url = "https://finfo-iboard.ssi.com.vn/graphql"
    headers = {"Content-Type": "application/json"}
    data = {
        "operationName": "companyProfile",
        "variables": {"symbol": "BCM", "language": "vn"},
        "query": "query companyProfile($symbol: String!, $language: String) {\n  companyProfile(symbol: $symbol, language: $language) {\n    symbol\n    subsectorcode\n    industryname\n    supersector\n    sector\n    subsector\n    foundingdate\n    chartercapital\n    numberofemployee\n    banknumberofbranch\n    companyprofile\n    listingdate\n    exchange\n    firstprice\n    issueshare\n    listedvalue\n    companyname\n    __typename\n  }\n  companyStatistics(symbol: $symbol) {\n    symbol\n    ttmtype\n    marketcap\n    sharesoutstanding\n    bv\n    beta\n    eps\n    dilutedeps\n    pe\n    pb\n    dividendyield\n    totalrevenue\n    profit\n    asset\n    roe\n    roa\n    npl\n    financialleverage\n    __typename\n  }\n}\n",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            result = await response.json()
            return result


# Run the async function
loop = asyncio.get_event_loop()
response_data = loop.run_until_complete(send_request())
print(response_data)

