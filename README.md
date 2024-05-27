# Stock Chatbot

## Description
This is a simple chatbot that allows users to select a stock exchange and view the top 5 stocks along with their current prices. The chatbot interface mimics a conversational experience similar to WhatsApp.

## Setup

1. Clone the repository:
    ```sh
    `git clone https://github.com/RevanthGhanta/chatbot.git`
    `cd chatbot`
    ```

2. Create and activate a virtual environment:
    ```sh
    `python -m venv venv`
    `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    `pip install -r requirements.txt`
    ```

4. Run the FastAPI application:
    ```sh
    `uvicorn app:app --reload --port 8001`
    ```

5. Open your web browser and go to `http://localhost:8001` to interact with the chatbot.

## Features
- Upon loading, it greets the user and provides a list of stock exchanges.
- Users can either type or select an exchange from the list displayed.
- Upon selecting an exchange, it shows a list of top stocks in that exchange.
- Users can either type or select a stock from the list displayed.
- Upon selecting a stock, it shows the current price and options to go back to the main menu or stock list.
- Basic error handling and user-friendly interface.
