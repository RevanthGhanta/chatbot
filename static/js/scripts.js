document.addEventListener('DOMContentLoaded', () => {
    const websocket = new WebSocket(`ws://${window.location.host}/ws`);

    const messages = document.getElementById('messages');
    const input = document.getElementById('input');
    const sendButton = document.getElementById('send');

    function appendMessage(message, type = 'system', data = null) {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${type}`;
        messageElement.textContent = message;
        if (data) {
            messageElement.dataset.value = data;
            messageElement.classList.add('clickable');
            messageElement.addEventListener('click', () => handleMessage(data, message));
        }
        messages.appendChild(messageElement);
        messages.scrollTop = messages.scrollHeight;
    }

    function showExchanges(exchanges) {
        appendMessage('Select an exchange:', 'system');
        exchanges.forEach(exchange => {
            appendMessage(`${exchange.code}: ${exchange.name}`, 'system', exchange.code);
        });
    }

    function showStocks(stocks) {
        appendMessage('Select a stock:', 'system');
        stocks.forEach(stock => {
            appendMessage(`${stock.code}: ${stock.stockName}`, 'system', stock.code);
        });
    }

    function showPrice(stock, price) {
        appendMessage(`The current price of ${stock} is ${price}`, 'system');
        const backButton = document.createElement('button');
        backButton.classList.add("back-button");
        backButton.textContent = 'Back';
        backButton.addEventListener('click', () => handleMessage('back'));
        messages.appendChild(backButton);

        const menuButton = document.createElement('button');
        menuButton.classList.add("menu-button");
        menuButton.textContent = 'Menu';
        menuButton.addEventListener('click', () => handleMessage('menu'));
        messages.appendChild(menuButton);
    }

    websocket.onmessage = function(event) {
        const message = JSON.parse(event.data);
        if (message.type === 'message') {
            appendMessage(message.data, 'system');
        } else if (message.type === 'exchanges') {
            showExchanges(message.data);
        } else if (message.type === 'stocks') {
            showStocks(message.data);
        } else if (message.type === 'price') {
            showPrice(message.data.stock, message.data.price);
        }
    };

    function handleMessage(data, message = null) {
        if (message) {
            appendMessage(`${message}`, 'user');
        }
        if (data.toLowerCase() === 'menu') {
            websocket.send('menu');
        } else if (data.toLowerCase() === 'back') {
            websocket.send('back');
        } else {
            websocket.send(data);
        }
    }

    input.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            const message = input.value.trim();
            input.value = '';
            appendMessage(`You: ${message}`, 'user');
            handleMessage(message);
        }
    });

    sendButton.addEventListener('click', () => {
        const message = input.value.trim();
        input.value = '';
        appendMessage(`You: ${message}`, 'user');
        handleMessage(message);
    });
});
