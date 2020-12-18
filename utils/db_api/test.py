import asyncio
import random
from utils.db_api.postgresql import Database


async def test():
    """Test for working with database queries"""
    print("Success!")


loop = asyncio.get_event_loop()
db = loop.run_until_complete(Database.create())
loop.run_until_complete(test())
