import asyncpg
from asyncpg.pool import Pool
from loguru import logger
from data import config


class Database:
    def __init__(self, pool):
        self.pool: Pool = pool

    @classmethod
    async def create(cls):
        pool = await asyncpg.create_pool(
            user=config.PGUSER,
            password=config.PGPASSWORD,
            host=config.IP,
            database="TextFromPictureDB"
        )
        return cls(pool)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num + 1}" for num, item in enumerate(parameters)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, user_id: int, username: str, name: str):
        try:
            sql = """
               INSERT INTO users(id, username, first_name) 
               VALUES($1, $2, $3);
               """
            await self.pool.execute(sql, user_id, username, name)
            logger.success(f'{user_id} - Successfully added to database[users]!')
        except asyncpg.exceptions.UniqueViolationError:
            pass
        except Exception as err:
            logger.exception(f'{user_id} - Unknown error while adding user to database[users]\n'
                             f'More details:\n'
                             f'{err}')

    async def get_user(self, user_id: int):
        try:
            sql = """
            SELECT * FROM users WHERE id = $1;
            """
            return await self.pool.fetchrow(sql, user_id)
        except:
            return None

    async def add_user_info(self, user_id: int):
        try:
            sql = """
               INSERT INTO user_info(user_id, registration_date) 
               VALUES($1, NOW());
               """
            await self.pool.execute(sql, user_id)
            logger.success(f'{user_id} - Successfully added to database[user_info]!')
        except Exception as err:
            logger.exception(f'{user_id} - Unknown error while adding user to database[user_info]\n'
                             f'More details:\n'
                             f'{err}')

    async def get_user_language(self, user_id: int):
        try:
            sql = """
            SELECT lang_code FROM user_info WHERE user_id = $1;
            """
            return await self.pool.fetchval(sql, user_id)
        except:
            return None