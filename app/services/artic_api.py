import httpx

BASE_URL = "https://api.artic.edu/api/v1/artworks"


def get_artwork(external_id: int):
    r = httpx.get(f"{BASE_URL}/{external_id}", timeout=5)

    if r.status_code != 200:
        return None

    data = r.json().get("data")
    if not data:
        return None

    return {
        "external_id": external_id,
        "title": data["title"]
    }