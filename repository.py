from sqlalchemy import select, update

from database import new_session, ProcessModel, InfoModel
from schemas import SProcessCreate, SProcess, SInfoAdd, SInfo


class ProcessRepository:
    @classmethod
    async def create_process(cls, data: SProcessCreate) -> int:
        async with new_session() as session:
            data_dict = data.model_dump()
            process = ProcessModel(**data_dict)
            session.add(process)
            await session.flush()
            await session.commit()
            return process.id

    @classmethod
    async def get_processes(cls, **filter_by) -> list[SProcess]:
        async with new_session() as session:
            stmt = select(ProcessModel).filter_by(**filter_by)
            result = await session.execute(stmt)
            process_models = result.scalars().all()
            process_schemas = [
                SProcess.model_validate(process_model)
                for process_model in process_models
            ]
            return process_schemas

    @classmethod
    async def update_process(cls, id: int, data: dict) -> int:
        async with new_session() as session:
            print(data)
            stmt = (
                update(ProcessModel)
                .values(**data)
                .filter_by(id=id)
                .returning(ProcessModel.id)
            )
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()


class InfoRepository:
    @classmethod
    async def add_info(cls, data: SInfoAdd) -> int:
        async with new_session() as session:
            data_dict = data.model_dump()
            info = InfoModel(**data_dict)
            session.add(info)
            await session.flush()
            await session.commit()
            return info.id

    @classmethod
    async def get_infos(cls, **filter_by) -> list[SInfo]:
        async with new_session() as session:
            stmt = select(InfoModel).filter_by(**filter_by)
            result = await session.execute(stmt)
            infos_models = result.scalars().all()
            infos_schemas = [
                SInfo.model_validate(info_model) for info_model in infos_models
            ]
            return infos_schemas
