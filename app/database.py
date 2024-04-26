from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, MappedAsDataclass

engine = create_async_engine("sqlite+aiosqlite:///processes.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase, MappedAsDataclass):
    pass


class ProcessModel(Model):
    __tablename__ = "processes"

    id: Mapped[int] = mapped_column(init=False, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(init=True, nullable=False)
    started_at: Mapped[datetime] = mapped_column(init=False, default=datetime.now(), nullable=False)
    finished_at: Mapped[datetime] = mapped_column(init=False, default=None, nullable=True)
    notified: Mapped[bool] = mapped_column(init=False, default=False, nullable=False)
    

class InfoModel(Model):
    __tablename__ = "info"

    id: Mapped[int] = mapped_column(init=False, primary_key=True, nullable=False)
    process_id: Mapped[int] = mapped_column(ForeignKey("processes.id"))
    message: Mapped[str] = mapped_column(init=True, nullable=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
