from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import json
import os

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load stock data from JSON file
with open('stock_data.json', 'r') as f:
    stock_data = json.load(f)

@app.get("/")
async def get():
    with open('static/index.html') as f:
        return HTMLResponse(f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    async def send_exchanges():
        exchanges = [{'code': exchange['code'], 'name': exchange['stockExchange']} for exchange in stock_data]
        await websocket.send_json({'type': 'exchanges', 'data': exchanges})

    async def send_stocks(exchange_code):
        for exchange in stock_data:
            if exchange['code'] == exchange_code:
                await websocket.send_json({'type': 'stocks', 'data': exchange['topStocks']})
                break

    async def send_price(exchange_code, stock_code):
        for exchange in stock_data:
            if exchange['code'] == exchange_code:
                for stock in exchange['topStocks']:
                    if stock['code'] == stock_code:
                        await websocket.send_json({'type': 'price', 'data': {'stock': stock['stockName'], 'price': stock['price']}})
                        break
                break

    await websocket.send_json({'type': 'message', 'data': 'Hello there! Welcome to the chatbot.'})
    await send_exchanges()

    current_exchange = None

    while True:
        data = await websocket.receive_text()
        if current_exchange is None:
            current_exchange = data.upper()
            await send_stocks(current_exchange)
        else:
            await send_price(current_exchange, data.upper())
            current_exchange = None
            await send_exchanges()