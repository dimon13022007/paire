import random
import asyncio
import aiohttp
from database.models import RegisterUser
from database.engine import async_sessions

languages = [
    "Python", "Java", "JavaScript", "PHP", "Go",
    "C,C++", "C#", "Swift", "Kotlin", "R"
]

industries = [
    "Backend", "Front-end", "FullStack", "GameDev", "MobileDev",
    "TelegramBots", "AI", "AppDev", "OSDev", "Cybersecurity",
    "Libraries", "BlockchainDev"
]

cities = ["New York", "Kyiv", "Berlin", "Tokyo", "Toronto", "Warsaw"]
names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"]
ages = list(range(18, 40))
texts = [None, "Just a dev", "Love Python", "Coffee addict", "C++ fan", ""]

def random_langs():
    selected = random.sample(languages, k=random.randint(1, 2))
    return selected + [None] * (2 - len(selected))

def random_inds():
    selected = random.sample(industries, k=random.randint(1, 3))
    return selected + [None] * (3 - len(selected))

async def fetch_image(session, url):
    async with session.get(url) as response:
        return await response.read()

async def generate_user(i: int, session: aiohttp.ClientSession) -> RegisterUser:
    user_name = random.randint(10**9, 10**10 - 1)
    city = random.choice(cities)
    name = random.choice(names)
    age = str(random.choice(ages))
    text_disc = random.choice(texts)

    lang = random_langs()
    ind = random_inds()

    # Використовуємо Lorem Picsum для отримання зображення
    img_url = f"https://picsum.photos/300/300?random={i}"
    img_bytes = await fetch_image(session, img_url)

    is_active = random.choice([True, False])
    is_blocked = random.choice([True, False])

    return RegisterUser(
        user_name=user_name,
        city=city,
        name=name,
        age=age,
        text_disc=text_disc,
        language=lang[0],
        language_2=lang[1],
        industry=ind[0],
        industry_1=ind[1],
        industry_2=ind[2],
        img=img_bytes,
        is_active=is_active,
        is_blocked=is_blocked
    )

async def insert_fake_users():
    async with aiohttp.ClientSession() as http_session:
        async with async_sessions() as db_session:
            users = []
            for i in range(100):
                user = await generate_user(i, http_session)
                users.append(user)
            db_session.add_all(users)
            await db_session.commit()
            print("✅ Inserted 100 users")

if __name__ == "__main__":
    asyncio.run(insert_fake_users())
