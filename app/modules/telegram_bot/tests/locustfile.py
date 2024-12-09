from locust import HttpUser, task, between

class TelegramBotUser(HttpUser):
    host = "https://api.telegram.org"
    wait_time = between(1, 5)

    @task
    def send_start_command(self):
        bot_token = "7318289178:AAGlwhBrbP-6RVSpx67k-B1izPLZYMIrRO0"
        self.client.post(
            f"/bot{bot_token}/sendMessage",
            json={
                "chat_id": 1410283342,
                "text": "/start"
            }
        )
