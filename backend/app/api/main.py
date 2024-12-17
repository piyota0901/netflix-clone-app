import uvicorn
from fastapi import FastAPI

from app.api.routers import movies

app = FastAPI()

@app.get(path="/")
async def health():
    """ヘルスチェック用のエンドポイント
    """
    return {"status": "ok"}

app.include_router(movies.router)

if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, reload=True)
