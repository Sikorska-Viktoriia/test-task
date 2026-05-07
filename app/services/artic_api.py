import httpx

BASE_URL = "https://api.artic.edu/api/v1/artworks"


async def get_artwork(external_id: int):

    async with httpx.AsyncClient() as client:

        response = await client.get(
            f"{BASE_URL}/{external_id}"
        )

    if response.status_code != 200:
        return None

    data = response.json().get("data")

    if not data:
        return None

    return {
        "external_id": data["id"],
        "title": data["title"]
    }