import uvicorn
from fastapi import APIRouter, Header, HTTPException, Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.cors import CORSMiddleware

from app.api.db_manegar import update_order
from app.api.db_models import AsyncSessionLocal

from app.api.models import OrderIn, OrderOut, OrderUpdate
from app.api import db_manegar, db_models

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You can restrict the HTTP methods if needed
    allow_headers=["*"],  # You can restrict the HTTP headers if needed
)


async def get_db():
    async_db = AsyncSessionLocal()
    try:
        yield async_db
    finally:
        await async_db.close()



@app.post('/')
async def add(order: OrderIn, db: AsyncSession = Depends(get_db)):

    await db_manegar.add_order(order, db)
    await db.commit()
    for instance in db:
        await db.refresh(instance)

    return {'message': "performance add"}


@app.get('/', response_model=list[OrderOut])
async def get_all_(db: AsyncSession = Depends(get_db)):
    return await db_manegar.get_all_order(db)


@app.get('/{id}', response_model=OrderIn)
async def get_one(id: int, db: AsyncSession = Depends(get_db)):
    return await db_manegar.get_order(id, db)




@app.put('/{id}', response_model=OrderIn)
async def update(id: int, performances: OrderUpdate, db: AsyncSession = Depends(get_db)):
    perfo = await db_manegar.get_order(id, db)
    if not perfo:
        raise HTTPException(status_code=404, detail="Not found")

    await update_order(id, performances.dict(exclude_unset=True), db)

    await db.commit()
    return await db_manegar.get_order(id, db)


@app.delete('/{id}')
async def delete(id: int, db: AsyncSession = Depends(get_db)):
    perfo = await db_manegar.get_order(id, db)
    if not perfo:
        raise HTTPException(status_code=404, detail="not found")

    await db_manegar.delete_order(id, db)

    await db.commit()
    for instance in db:
        await db.refresh(instance)
    return {'message': 'performance delete'}


if __name__ == "__main__":
    uvicorn.run(app, port=9000)