from locust import HttpUser, task, between
from decouple import config


class TelegramBotUser(HttpUser):
    host = "https://api.telegram.org"
    wait_time = between(1, 5)

    @task
    def send_start_command(self):
        bot_token = config('TELEGRAM_BOT_TOKEN')
        self.client.post(
            f"/bot{bot_token}/sendMessage",
            json={
                "chat_id": 1410283342,
                "text": "/start"
            }
        )
