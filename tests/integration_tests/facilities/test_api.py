from httpx import AsyncClient


async def test_get_facilities(ac: AsyncClient):
    response = await ac.get(
        url="/api/v1/facilities"
    )
    
    assert response.status_code == 200
    assert isinstance(response.json()["data"], list)
    
    
async def test_create_facility(ac: AsyncClient):
    facility_title = "Free breakfast"
    response = await ac.post(
        url="/api/v1/facilities",
        json={
            "title": facility_title
        }
    )
    
    data = response.json()["data"]
    
    assert response.status_code == 200
    assert isinstance(data, dict)
    assert data["title"] == facility_title
