from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine,  async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import asyncio

class ContextDB:

    def __init__(self, DATABASE_URL):

        self.__DATABASE_URL__ = DATABASE_URL

        self.engine_ = None

        self.session_ = None
        

    def engine_create(self):
    
        self.engine_ = create_async_engine(
            self.__DATABASE_URL__,

            connect_args= {"check_same_thread" : False,
                           'timeout': 5},

            echo= True
        )

        return self.engine_


    def session(self):

        self.session_ = async_sessionmaker(autoflush=False,
                                        bind=self.engine_,
                                        class_=AsyncSession)()

        return self.session_
    
    
    async def create_all_table(self):

        async with settings_db.engine_.begin() as conn:

                await conn.run_sync(Base.metadata.create_all)    

class Base(DeclarativeBase):

    pass



settings_db = ContextDB("sqlite+aiosqlite:///./test.db")

engine = settings_db.engine_create()

settings_db.session()

settings_db.create_all_table()
