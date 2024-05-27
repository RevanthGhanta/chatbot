# Stock Chatbot

## Description
This is a simple chatbot that allows users to select a stock exchange and view the top 5 stocks along with their current prices. The chatbot interface mimics a conversational experience similar to WhatsApp.

## Setup

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd chatbot
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Run the FastAPI application:
    ```sh
    uvicorn app:app --reload
    ```

5. Open your web browser and go to `http://localhost:8000` to interact with the chatbot.

## Features
- Upon loading, it greets the user and provides a list of stock exchanges.
- Users can either type or select an exchange from the list displayed.
- Upon selecting an exchange, it shows a list of top stocks in that exchange.
- Users can either type or select a stock from the list displayed.
- Upon selecting a stock, it shows the current price and options to go back to the main menu or stock list.
- Basic error handling and user-friendly interface.

## Optional Enhancements
- Add error handling for invalid inputs.
- Implement user authentication.
- Store user preferences and chat history.
- Optimize for performance and scalability.
