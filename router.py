from typing import Annotated

from fastapi import APIRouter, Depends

from repository import ProcessRepository, InfoRepository
from schemas import SProcessCreate, SProcess, SProcessId, SInfoAdd, SInfoId

process_router = APIRouter(prefix="/processes", tags=['Процессы'])


@process_router.post("")
async def create_process(process: Annotated[SProcessCreate, Depends()]) -> SProcessId:
    process_id = await ProcessRepository.create_process(process)
    return SProcessId(process_id=process_id)


@process_router.get("")
async def get_processes() -> list[SProcess]:
    processes = await ProcessRepository.get_all_processes()
    return processes


info_router = APIRouter(prefix="/info", tags=["Информационные сообщения"])


@info_router.post("")
async def add_info(info: Annotated[SInfoAdd, Depends()]) -> SInfoId:
    info_id = await InfoRepository.add_info(info)
    return SInfoId(info_id=info_id)
