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

    async def add_user_info(self, user_id: int, lang_code: str = 'en'):
        try:
            sql = """
               INSERT INTO user_info(user_id, registration_date, lang_code) 
               VALUES($1, NOW(), $2);
               """
            await self.pool.execute(sql, user_id, lang_code)
            logger.success(f'{user_id} - Successfully added to database[user_info]!')
        except Exception as err:
            logger.exception(f'{user_id} - Unknown error while adding user to database[user_info]\n'
                             f'More details:\n'
                             f'{err}')

    async def get_users_quantity(self):
        try:
            sql = """
            SELECT COUNT(*) FROM users;
            """
            return await self.pool.fetchval(sql)
        except:
            return None

    async def get_user_info(self, user_id: int):
        try:
            sql = """
            SELECT * FROM user_info WHERE user_id = $1;
            """
            return await self.pool.fetchrow(sql, user_id)
        except:
            return None

    async def get_user_language(self, user_id: int):
        try:
            sql = """
            SELECT lang_code FROM user_info WHERE user_id = $1;
            """
            return await self.pool.fetchval(sql, user_id)
        except:
            return None

    async def get_users_by_language(self, lang_code: str):
        try:
            if lang_code == 'all':
                sql = """
                SELECT * from user_info;
                """
                return await self.pool.fetch(sql)
            else:
                sql = """
                SELECT * from user_info WHERE lang_code = $1;
                """
                return await self.pool.fetch(sql, lang_code)
        except:
            return None

    async def change_language(self, user_id: int, lang_code: str):
        try:
            sql = """
                UPDATE user_info SET lang_code = $2 WHERE user_id = $1;
                """
            await self.pool.execute(sql, user_id, lang_code)
            logger.success(f'{user_id} - Successfully updated in database[user_info.lang_code]!')
        except Exception as err:
            logger.exception(f'{user_id} - Unknown error while updating in database[user_info.lang_code]\n'
                             f'More details:\n'
                             f'{err}')

    async def add_user_to_blacklist(self, user_id: int):
        try:
            sql = """
               INSERT INTO blacklist(user_id) 
               VALUES($1);
               """
            await self.pool.execute(sql, user_id)
            logger.success(f'{user_id} - Successfully added to database[blacklist]!')
        except asyncpg.exceptions.UniqueViolationError:
            raise asyncpg.exceptions.UniqueViolationError
        except Exception as err:
            logger.exception(f'{user_id} - Unknown error while adding user to database[blacklist]\n'
                             f'More details:\n'
                             f'{err}')

    async def remove_user_from_blacklist(self, user_id: int):
        sql = """
        DELETE FROM blacklist WHERE user_id = $1;
        """
        await self.pool.execute(sql, user_id)
        logger.success(f'{user_id} - Successfully removed from database[blacklist]!')

    async def get_user_from_blacklist(self, user_id: int):
        try:
            sql = """
            SELECT user_id FROM blacklist WHERE user_id = $1;
            """
            return await self.pool.fetchval(sql, user_id)
        except:
            return None

    async def add_user_photo(self, user_id: int, photo_id: str):
        try:
            sql = """
               INSERT INTO user_photos(user_id, photo_id, datetime) 
               VALUES($1, $2, NOW());
               """
            await self.pool.execute(sql, user_id, photo_id)
            logger.success(f'{user_id} - Successfully added to database[user_photos]!')
        except asyncpg.exceptions.UniqueViolationError:
            raise asyncpg.exceptions.UniqueViolationError
        except Exception as err:
            logger.exception(f'{user_id} - Unknown error while adding user to database[user_photos]\n'
                             f'More details:\n'
                             f'{err}')

    async def get_user_photos(self, user_id: int, limit: int = 5):
        try:
            sql = """
            SELECT * FROM user_photos WHERE user_id = $1 ORDER BY datetime DESC LIMIT $2;
            """
            return await self.pool.fetch(sql, user_id, limit)
        except:
            return None

    async def add_photo_text(self, user_id: int, photo_id: str, text: str):
        try:
            sql = """
                UPDATE user_photos SET text = $2 WHERE photo_id = $1;
                """
            await self.pool.execute(sql, photo_id, text)
            logger.success(f'{user_id} - Successfully updated in database[user_photos.text]!')
        except Exception as err:
            logger.exception(f'{user_id} - Unknown error while updating in database[user_photos.text]\n'
                             f'More details:\n'
                             f'{err}')

    async def get_photo(self, photo_id: str):
        try:
            sql = """
            SELECT text FROM user_photos WHERE photo_id = $1;
            """
            return await self.pool.fetchval(sql, photo_id)
        except:
            return None

    async def checking_user_subscribe(self, user_id: int):
        try:
            sql = """
            SELECT * FROM subscriptions WHERE (user_id = $1) and (date_to > NOW()) ORDER BY id DESC LIMIT 1;
            """
            response = await self.pool.fetchrow(sql, user_id)
            if response:
                return True
            return False
        except:
            return False

    async def get_user_subscribes(self, user_id: int):
        try:
            sql = """
            SELECT * FROM subscriptions WHERE user_id = $1 ORDER BY id DESC;
            """
            return await self.pool.fetch(sql, user_id)
        except:
            return None

    async def api_requests_per_day(self, user_id: int):
        try:
            sql = """
            SELECT count(*) FROM user_photos WHERE (user_id = $1) and (CURRENT_DATE = datetime::date);
            """
            requests = await self.pool.fetchval(sql, user_id)
            if requests <= 5:
                return True
            return False
        except:
            return False

    async def add_user_donate(self, user_id: int, amount: str, currency: str, message: str = None):
        try:
            sql = """
                INSERT INTO donations(user_id, amount, currency, message, datetime)
                VALUES ($1, $2, $3, $4, NOW());
                """
            await self.pool.execute(sql, user_id, amount, currency, message)
            logger.success(f'{user_id} - Successfully added to database[donations]!')
        except Exception as err:
            logger.exception(f'{user_id} - Unknown error while adding to database[donations]\n'
                             f'More details:\n'
                             f'{err}')

    async def get_user_donations(self, user_id: int):
        try:
            sql = """
            SELECT * FROM donations WHERE user_id = $1 ORDER BY id DESC;
            """
            return await self.pool.fetch(sql, user_id)
        except:
            return None

    async def add_user_subscription(self, user_id: int, date_to: str = '30'):
        try:
            sql = f"""
                INSERT INTO subscriptions(user_id, donation_id, date_to)
                VALUES ($1, 
                (SELECT id FROM donations WHERE user_id = $1 ORDER BY id DESC LIMIT 1), 
                (NOW() + interval '{date_to} day'));
                """
            await self.pool.execute(sql, user_id)
            logger.success(f'{user_id} - Successfully added to database[subscriptions]!')
        except Exception as err:
            logger.exception(f'{user_id} - Unknown error while adding to database[subscriptions]\n'
                             f'More details:\n'
                             f'{err}')
