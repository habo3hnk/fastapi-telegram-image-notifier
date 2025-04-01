from database.session import AsyncSessionManager
from config.config import DATABASE_URL


database = AsyncSessionManager(DATABASE_URL, echo=True)
