from fastapi import Depends, HTTPException, status, APIRouter, Response
import asyncio
from concurrent.futures import ThreadPoolExecutor
from kafka import KafkaProducer
from app.crawl import get_stock_company_profile, get_stock_prices, get_stock_shareholders
router = APIRouter()

executor = ThreadPoolExecutor()

# Kafka producer setup
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Asynchronously execute the crawl functions
async def execute_crawl_functions():
    loop = asyncio.get_running_loop()

    # Submit the crawl functions to the executor
    future_profile = loop.run_in_executor(executor, get_stock_company_profile)
    future_shareholders = loop.run_in_executor(executor, get_stock_shareholders)
    future_price = loop.run_in_executor(executor, get_stock_prices)

    # Await completion of all crawl functions
    results = await asyncio.gather(future_profile, future_shareholders, future_price)

    # Send the results to Kafka
    for result in results:
        producer.send('crawl_results', value=result)

router.get("/stock")
async def crawl():
    await execute_crawl_functions()
    return {"message": "Fetching data..." }