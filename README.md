# Data Service

The Data Service API provides functionality for managing public holidays, stock data crawling, and derivative stock information retrieval.

## Features

### Public Holidays
- Handle user's crud holiday data,return a list of public holidays and weekends (Saturday & Sunday) in the specified year.

### Stock Data
- Get information about a stock with the given stock code, including company description, list of shareholders, history prices

### Derivative Codes
- In Viet Nam, the derivative expiration falls on Thursday, the third week of the expiration month, which includes the current month, the next month, and the last month of the two most recent quarters
- Let user input specific day and get a list of derivative codes based on that day
- The derivative stock codes follow the format: {
                    "symbol": "VN30F2306",
                    "code": "VN30F1M",
                    "expired_date": "15/06/2023"
                }

## Additional Resources
- https://iboard.ssi.com.vn/
- [Rules for Generating Derivative Stock Codes](https://online.hsc.com.vn/phai-sinh/cach-doc-ma-hdtl.html)                


