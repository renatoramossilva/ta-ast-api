from playwright.async_api import async_playwright
from fastapi import APIRouter, HTTPException
from app.api.endpoints.services import (
    get_info,
    transform_search_name,
    convert_comma_to_dot,
    Hotel,
)
from app.database import crud

router = APIRouter()


@router.get("/scrape")
async def scrape(hotel_name: str) -> dict:
    """
    Scrape booking.com using playwright

    **Request Body:**
    - `hotel_name` (str): The name of the hotel to search for.

    **Returns:**
        dict: A dictionary containing the hotel's name, address, description, and review score.
    """
    async with async_playwright() as p:
        page_url = (
            "https://www.booking.com/searchresults.es.html?ss="
            + transform_search_name(hotel_name)
        )

        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(page_url, timeout=60000)

        url = await page.query_selector(
            'div[data-testid="property-card-container"] div div a'
        )

        return await get_info(await url.get_attribute("href"))


@router.post("/post")
async def post(hotel_name):
    async with async_playwright() as p:
        page_url = (
            "https://www.booking.com/searchresults.es.html?ss="
            + transform_search_name(hotel_name)
        )
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(page_url, timeout=60000)

        url = await page.query_selector(
            'div[data-testid="property-card-container"] div div a'
        )
        hotel_data = await get_info(await url.get_attribute("href"))
        saved_hotel = crud.create_hotel(
            name=hotel_data["name"],
            address=hotel_data["address"],
            description="some description",
            review=convert_comma_to_dot(hotel_data["review"]),
            db=crud.get_db(),
        )

    return {"message": "Hotel data saved successfully", "hotel": saved_hotel}


@router.post("/save")
async def save(hotel: Hotel):
    try:
        saved_hotel = crud.create_hotel(
            name=hotel.name,
            address=hotel.address,
            description=hotel.description,
            review=hotel.review,
            db=crud.get_db(),
        )
        return {"message": "Hotel data saved successfully", "hotel": saved_hotel}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
