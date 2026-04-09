from httpx import AsyncClient
import pytest
from tests.conftest import get_db_null_pool


@pytest.fixture(scope="module")
async def delete_all_bookings():
    async for _db in get_db_null_pool():
        await _db.bookings.delete()
        await _db.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2026-05-01", "2026-05-10", 200),
        (1, "2026-05-01", "2026-05-10", 200),
        (1, "2026-05-01", "2026-05-10", 200),
        (1, "2026-05-01", "2026-05-10", 200),
        (1, "2026-05-01", "2026-05-10", 200),
        (1, "2026-05-01", "2026-05-10", 409),
    ],
)
async def test_create_booking(
    room_id,
    date_from,
    date_to,
    status_code,
    authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.post(
        url="/api/v1/bookings",
        json={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )
    data = response.json()

    assert response.status_code == status_code
    if status_code == 200:
        assert isinstance(data, dict)
        assert data["data"]["room_id"] == room_id
        assert data["status"] == "OK"


@pytest.mark.parametrize(
    "room_id, date_from, date_to, total_bookings",
    [
        (1, "2026-05-01", "2026-05-10", 1),
        (1, "2026-05-01", "2026-05-10", 2),
        (1, "2026-05-01", "2026-05-10", 3),
        (1, "2026-05-01", "2026-05-10", 4),
    ],
)
async def test_add_and_get_my_bookings(
    room_id,
    date_from,
    date_to,
    total_bookings,
    delete_all_bookings,
    authenticated_ac: AsyncClient,
):
    res_bookings = await authenticated_ac.post(
        url="api/v1/bookings",
        json={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )

    assert res_bookings.status_code == 200

    res_user_bookings = await authenticated_ac.get(url="api/v1/bookings/me")
    data = res_user_bookings.json()

    assert res_user_bookings.status_code == 200
    assert len(data) == total_bookings
