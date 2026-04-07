from httpx import AsyncClient


async def test_get_hotels(ac: AsyncClient):
    response = await ac.get(
        url="api/v1/hotels", params={"date_from": "2026-05-01", "date_to": "2026-05-10"}
    )

    assert response.status_code == 200
