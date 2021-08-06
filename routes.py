from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse

from container import Container
from ports import Ports

api_router: APIRouter = APIRouter(default_response_class=ORJSONResponse)


@api_router.get(
    "/test",
    summary="test",
    responses={
        200: {
            "description": "Получение списка сотрудников",
        },
    },
    status_code=200,
)
@inject
async def test(
    ports: Ports = Depends(Provide[Container.test_ports])
):
    return ORJSONResponse(content=ports.test())
