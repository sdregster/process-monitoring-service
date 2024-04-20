from sqlalchemy import select

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
    async def get_all_processes(cls) -> list[SProcess]:
        async with new_session() as session:
            query = select(ProcessModel)
            result = await session.execute(query)
            process_models = result.scalars().all()
            process_schemas = [SProcess.model_validate(process_model) for process_model in process_models]
            return process_schemas


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
    async def get_infos(cls) -> list[SInfo]:
        async with new_session() as session:
            query = select(InfoModel)
            result = await session.execute(query)
            infos_models = result.scalars().all()
            infos_schemas = [SInfo.model_validate(info_model) for info_model in infos_models]
            return infos_schemas
