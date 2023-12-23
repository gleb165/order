from sqlalchemy.ext.asyncio import AsyncSession

from app.api.models import OrderUpdate, OrderIn, OrderOut
from app.api.db_models import Order
import requests

# model for performance


async def add_order(per: OrderIn, db: AsyncSession):

    api_url1 = f"http://127.0.0.1:8000/{per.show_id}"
    api_url2 = f"http://127.0.0.1:5000/user/{per.user_id}"
    api_url3 = f"http://127.0.0.1:8000/subtract_tickets/{per.amount}/{per.show_id}"
    user_url = f"http://127.0.0.1:5000/email/{per.user_id}/{per.amount}"

    response1 = requests.get(api_url1)
    response2 = requests.get(api_url2)

    if response1.status_code == 200 and response2.status_code == 200 and requests.get(api_url3).status_code == 200 and requests.post(user_url).status_code == 200:

        return await db.execute(Order.insert().values(**per.dict()))
        # Process the product data
    else:
        print(f"Error: {response1.status_code}")


async def get_all_order(db: AsyncSession):
    return (await db.execute(Order.select())).all()

async def get_order(id: int, db: AsyncSession):
    return (await db.execute(Order.select(Order.c.id == id))).fetchone()


async def delete_order(id: int, db: AsyncSession):
    query = Order.delete().where(Order.c.id == id)
    return await db.execute(query)


async def update_order(id: int, pla: OrderIn, db: AsyncSession):

    return await db.execute(Order
                            .update()
                            .where(Order.c.id == id)
                            .values(**pla))

#
# # model for shows
# # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#
# async def add_shows(pla: showsIn , db: AsyncSession):
#     return await db.execute(show.insert().values(**pla.dict()))
#
#
# async def get_all_shows(db: AsyncSession):
#     return (await db.execute(show.select())).all()
#
#     #return await database.fetch_all(query=performances.select())
#
#
# async def get_shows(id: int, db: AsyncSession):
#     return (await db.execute(show.select(show.c.id == id))).fetchone()
#
#
# async def delete_shows(id: int, db: AsyncSession):
#     query = show.delete().where(show.c.id == id)
#     return await db.execute(query)
#
#
# async def update_shows(id: int, sh: showsIn, db: AsyncSession):
#
#     return await db.execute(show
#                             .update()
#                             .where(show.c.id == id)
#                             .values(**sh))