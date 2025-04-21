import base64

from fastapi import FastAPI, UploadFile, Form, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import shutil
from fastapi import Request
from starlette.responses import HTMLResponse, RedirectResponse
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.models import RegisterUser
from database.session import get_async_session
from io import BytesIO
import base64
from database.models import Advertisement, RegisterUser
from database.engine import get_async_session
import os


app = FastAPI()


@app.post("/admin/user/{user_id}")
async def delete_user(user_id: int, request: Request, session: AsyncSession = Depends(get_async_session)):
    user = await session.get(RegisterUser, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await session.delete(user)
    await session.commit()

    return HTMLResponse(
        content=f"<h3>Пользователь удалён. <a href='/admin/users'>Назад к списку</a></h3>",
        status_code=200
    )

@app.get("/admin/users", response_class=HTMLResponse)
async def get_all_users(session: AsyncSession = Depends(get_async_session)):
    users = await session.execute(select(RegisterUser))
    users = users.scalars().all()

    html = """
    <html>
    <head>
        <title>Анкеты пользователей</title>
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                background-color: #f9f9f9;
                color: #333;
                padding: 40px;
            }
            .user-card {
                background-color: white;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
                padding: 20px;
                margin-bottom: 30px;
                display: flex;
                gap: 20px;
                align-items: flex-start;
            }
            .user-card img {
                border-radius: 8px;
                width: 180px;
                height: auto;
                object-fit: cover;
            }
            .user-info {
                flex: 1;
            }
            .user-info h2 {
                margin: 0;
                font-size: 22px;
                color: #222;
            }
            .user-info p {
                margin: 5px 0;
                color: #555;
            }
            .user-info .meta {
                font-size: 14px;
                color: #888;
            }
            .delete-button {
                margin-top: 10px;
                padding: 8px 14px;
                background-color: #ff4d4f;
                color: white;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                transition: background 0.2s ease;
            }
            .delete-button:hover {
                background-color: #d9363e;
            }
        </style>
    </head>
    <body>
        <h1>👥 Анкеты пользователей</h1>
    """

    for user in users:
        encoded_image = base64.b64encode(user.img).decode("utf-8")
        html += f"""
            <div class="user-card">
                <img src="data:image/jpeg;base64,{encoded_image}" alt="User Image"/>
                <div class="user-info">
                    <h2>{user.name}, {user.age}</h2>
                    <p class="meta">{user.industry} | {user.language}</p>
                    <p>{user.text_disc or ''}</p>
                    <form action="/admin/user/{user.id}" method="post">
                        <input type="hidden" name="_method" value="delete" />
                        <button type="submit" class="delete-button">Удалить</button>
                    </form>
                </div>
            </div>
        """

    html += "</body></html>"
    return html

@app.get("/admin/ads", response_class=HTMLResponse)
async def get_ad_page(session: AsyncSession = Depends(get_async_session)):
    ad = await session.scalar(select(Advertisement).order_by(Advertisement.id.desc()).limit(1))

    html = f"""
    <html>
    <head>
        <title>Реклама</title>
        <style>
            body {{
                font-family: 'Segoe UI', sans-serif;
                padding: 30px;
                background: #f9f9f9;
                color: #333;
            }}
            form {{
                background: #fff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.05);
                max-width: 600px;
            }}
            textarea {{
                width: 100%;
                font-size: 14px;
                padding: 10px;
                border-radius: 6px;
                border: 1px solid #ccc;
            }}
            input[type="file"] {{
                margin-top: 10px;
            }}
            button {{
                background: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                margin-top: 15px;
                cursor: pointer;
            }}
            button:hover {{
                background: #45a049;
            }}
        </style>
    </head>
    <body>
        <h2>📰 Редактор рекламы</h2>
        <form action="/admin/ads" method="post" enctype="multipart/form-data">
            <label>Текст рекламы:</label><br>
            <textarea name="text" rows="5">{ad.text if ad else ''}</textarea><br><br>
            <label>Загрузить картинку (необязательно):</label><br>
            <input type="file" name="image"><br><br>
            <button type="submit">💾 Сохранить</button>
        </form>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

@app.post("/admin/ads")
async def update_ad(
    text: str = Form(...),
    image: UploadFile = None,
    session: AsyncSession = Depends(get_async_session)
):
    image_path = None

    if image and image.filename:
        os.makedirs("media", exist_ok=True)
        image_path = f"media/ad_{image.filename}"
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    ad = await session.scalar(select(Advertisement).order_by(Advertisement.id.desc()).limit(1))
    if ad:
        ad.text = text
        if image_path:
            ad.image_path = image_path
    else:
        ad = Advertisement(text=text, image_path=image_path)
        session.add(ad)

    await session.commit()
    return RedirectResponse("/admin/ads", status_code=303)
