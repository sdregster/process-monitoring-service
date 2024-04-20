from typing import Annotated
from datetime import datetime

from fastapi import APIRouter, Depends

from repository import ProcessRepository, InfoRepository
from schemas import (
    SProcessCreate,
    SProcess,
    SProcessId,
    SInfoAdd,
    SInfoId,
    SInfo,
)

process_router = APIRouter(prefix="/processes", tags=["Процессы"])


@process_router.post("")
async def start_new_process(
    process: Annotated[SProcessCreate, Depends()]
) -> SProcessId:
    process_id = await ProcessRepository.create_process(process)
    return SProcessId(process_id=process_id)


@process_router.get("/unnotified")
async def get_unnotified_processes() -> list[SProcess]:
    processes = await ProcessRepository.get_processes(notified=False)
    return processes


@process_router.get("/finished/{process_id}")
async def mark_as_finished(process_id) -> dict:
    data = {"finished_at": datetime.now()}
    await ProcessRepository.update_process(process_id, data)
    return {"ok": True}


@process_router.get("/notified/{process_id}")
async def mark_as_notified(process_id) -> dict:
    data = {"notified": True}
    await ProcessRepository.update_process(process_id, data)
    return {"ok": True}


info_router = APIRouter(prefix="/info", tags=["Информационные сообщения"])


@info_router.post("")
async def add_new_info_message(info: Annotated[SInfoAdd, Depends()]) -> SInfoId:
    info_id = await InfoRepository.add_info(info)
    return SInfoId(info_id=info_id)


@info_router.get("/{process_id}")
async def get_info_messages_by_process_id(process_id: int) -> list[SInfo]:
    infos = await InfoRepository.get_infos(process_id=process_id)
    return infos
