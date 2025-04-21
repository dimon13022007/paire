import asyncio

likes_memory = {}
liked_users = {}
mutual_likes = set()
disliked_users = {}


async def auto_clear_memory():
    while True:
        await asyncio.sleep(86400)
        print("🧹 Очищаем временные лайки/дизлайки из памяти...")
        liked_users.clear()
        likes_memory.clear()
        mutual_likes.clear()

async def auto_clear_dislikes_only():
    while True:
        await asyncio.sleep(600)
        print("🧹 Очищаем только дизлайки из памяти...")
        disliked_users.clear()


