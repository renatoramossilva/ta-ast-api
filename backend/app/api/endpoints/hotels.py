from playwright.async_api import async_playwright
from fastapi import APIRouter
from app.api.endpoints.services import get_info, transform_search_name

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
        page_url = "https://www.booking.com/searchresults.es.html?ss=" + transform_search_name(hotel_name)

        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(page_url, timeout=60000)

        url = await page.query_selector('div[data-testid="property-card-container"] div div a')

        return await get_info(await url.get_attribute("href"))
