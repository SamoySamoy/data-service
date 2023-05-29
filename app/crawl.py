import requests
import json
from bs4 import BeautifulSoup
url = "https://finfo-iboard.ssi.com.vn/graphql"

# fetch the stock's company description
def get_stock_company_profile(stock: str):
    payload = json.dumps({
    "operationName": "companyProfile",
    "variables": {
        "symbol": stock,
        "language": "vn"
    },
    "query": "query companyProfile($symbol: String!, $language: String) {\n  companyProfile(symbol: $symbol, language: $language) {\n    symbol\n    subsectorcode\n    industryname\n    supersector\n    sector\n    subsector\n    foundingdate\n    chartercapital\n    numberofemployee\n    banknumberofbranch\n    companyprofile\n    listingdate\n    exchange\n    firstprice\n    issueshare\n    listedvalue\n    companyname\n    __typename\n  }\n  companyStatistics(symbol: $symbol) {\n    symbol\n    ttmtype\n    marketcap\n    sharesoutstanding\n    bv\n    beta\n    eps\n    dilutedeps\n    pe\n    pb\n    dividendyield\n    totalrevenue\n    profit\n    asset\n    roe\n    roa\n    npl\n    financialleverage\n    __typename\n  }\n}\n"
})
    headers = {
        'Accept': 'application/vnd.github+json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
        'Content-Type': 'application/json',
        'Cookie': '__cf_bm=.uP_FP0tcppzCjuQCIf_yncTYWQjVYye6rzL_C2FX.8-1685323698-0-AZ9xW26q88hLUZ7LOowxT3poSha2ekiNctcIZH8fXO7p1j6fqF7tqo4YdKa8dYFKQATZxjg9U0uMIjp3LOlR9ko='
    }

    response = requests.request("POST", url, headers=headers, data=payload).json()
    company_desc = response["data"]["companyProfile"]["companyprofile"]
    soup = BeautifulSoup(company_desc, 'html.parser')
    return soup.get_text()







