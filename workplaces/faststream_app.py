from faststream import App, RabbitBroker
import os
from aiogram import Bot, Dispatcher
import asyncio

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher(bot)

broker = RabbitBroker(os.getenv("RABBITMQ_URL"))

app = App(broker=broker)


@app.on_message(queue="user_events")
async def handle_user_login_event(message):
    data = message.json()
    if data.get("event") == "user_login":
        user_id = data.get("user_id")
        token = data.get("token")
        await bot.send_message(
            chat_id=int(os.getenv("USER_CHAT_ID")),
            text=f"User {user_id} logged in with token {token}",
        )
    await message.ack()


if __name__ == "__main__":
    app.run()
