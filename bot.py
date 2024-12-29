import httpx
import logging


logging.getLogger("httpx").disabled = True

class TelegramBot:
    def __init__(self, token: str):
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.offset = 0
        self.handlers = []

    def get_updates(self):
        """Get updates from Telegram"""
        try:
            response = httpx.get(
                f"{self.base_url}/getUpdates",
                params={"offset": self.offset, "timeout": 30},
                timeout=40,
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            logging.error(f"Request error while fetching updates: {e}")
            return {"result": []}

    def process_updates(self, updates):
        """Process incoming updates"""
        for update in updates.get("result", []):
            self.offset = update["update_id"] + 1
            if "message" in update:
                message = update["message"]
                # logging.info(f"Processing message: {message.get('text', '')}")
                logging.info()
                self.handle_message(message)
    def get_me(self):
        """Get bot info"""
        url = self.base_url + "/getMe"
        response = httpx.get(url)
        return response.json()
    
    def send_message(self, chat_id, text):
        """Send a message to the user"""
        url = self.base_url + f"/sendMessage?chat_id={chat_id}&text={text}"
        response = httpx.get(url)
        return response.json()

    def handle_message(self, message):
        """Process the message with the registered handlers"""
        for handler in self.handlers:
            if handler["text"] in message.get("text", ""):
                handler["function"](message)

    def message_handler(self, text):
        """Decorator to register a message handler function"""
        def decorator(function):
            self.handlers.append({"text": text, "function": function})
            return function
        return decorator

    def run(self):
        """Start the bot and process updates"""
        username = self.get_me()["result"]["username"]
        logging.info(f"@{username} is running")
        while True:
            try:
                updates = self.get_updates()
                if updates.get("result"):
                    self.process_updates(updates)
            except Exception as e:
                logging.error(f"Error in main loop: {e}")
