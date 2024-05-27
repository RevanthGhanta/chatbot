from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import json
import sys
from datetime import datetime

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load stock data from JSON file
try:
    with open('stock_data.json', 'r') as f:
        stock_data = json.load(f)
        # Proceed with processing the loaded JSON data
        print("File loaded successfully!")
except FileNotFoundError:
    print("Error: File not found.")
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)

# List to store messages
messages = []

# Function to save messages to a file
def save_messages():
    with open('messages.json', 'w') as f:
        json.dump(messages, f)

# Function to send a message to the client
async def send_message(websocket: WebSocket, message):
    await websocket.send_text(message)
    # Save the message
    messages.append({'timestamp': datetime.now().isoformat(), 'message': message})
    save_messages()

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
        global prev_exchange
        for exchange in stock_data:
            if exchange['code'] == exchange_code:
                for stock in exchange['topStocks']:
                    if stock['code'] == stock_code:
                        prev_exchange = exchange_code
                        await websocket.send_json({'type': 'price', 'data': {'stock': stock['stockName'], 'price': stock['price']}})
                        break
                break

    async def send_back():
        await send_stocks(prev_exchange)

    await send_message(websocket, 'Hello there! Welcome to the chatbot.')
    await send_exchanges()

    current_exchange = None

    while True:
        data = await websocket.receive_text()
        if data == 'back':
            await send_back()
        elif data == 'menu':
            await send_exchanges()
            current_exchange = None
        if current_exchange is None:
            if data.lower() != 'back' and data.lower() != 'menu':
                current_exchange = data.upper()
            await send_stocks(current_exchange)
        else:
            await send_price(current_exchange, data.upper())
