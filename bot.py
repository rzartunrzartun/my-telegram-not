import asyncio
import random
from groq import Groq
from telethon import TelegramClient, events

# ----------------- CONFIGURATION -----------------
GROQ_API_KEY = "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"
TELEGRAM_API_ID = 39253179
TELEGRAM_API_HASH = "c28f385c518482d7e94dd0163615cb0a"
# --------------------------------------------------

groq_client = Groq(api_key=GROQ_API_KEY)
client = TelegramClient("my_telegram_session", TELEGRAM_API_ID, TELEGRAM_API_HASH)


@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    if event.is_private:
        user_text = event.raw_text

        wait_seconds = random.randint(5, 10)
        await asyncio.sleep(wait_seconds)

        async with client.action(event.chat_id, "typing"):
            try:
                chat_completion = groq_client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are replying as me to a close friend on Telegram. "
                                "Reply naturally and casually in short Burmese (1 sentence or a few words). "
                                "Don't sound like a formal AI or bot."
                            ),
                        },
                        {"role": "user", "content": user_text},
                    ],
                    model="llama-3.1-8b-instant",  # အမှန်သို့ ပြင်ထားပါသည်
                )

                reply_text = chat_completion.choices[0].message.content.strip()

                await asyncio.sleep(2)
                await event.reply(reply_text)
                print(f"Replied: {user_text} -> {reply_text}")

            except Exception as e:
                print(f"Error: {e}")


print("Userbot is running... Press Ctrl+C to stop.")
client.start()
client.run_until_disconnected()