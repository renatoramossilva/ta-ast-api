"""
Endpoints for scraping and saving hotel data.
"""

from typing import Dict, Union

from app.api.endpoints.logger import setup_logger
from app.api.endpoints.services import Hotel, get_info, transform_search_name
from app.database import crud
from fastapi import APIRouter, HTTPException
from playwright.async_api import async_playwright

router = APIRouter()

BOOKING_URL = "https://www.booking.com/searchresults.es.html?ss="

LOG = setup_logger("ta-ast-hotels")


@router.get("/api/hotels/scrape")
async def scrape(hotel_name: str) -> Dict[str, Union[str, float, None]]:
    """
    Scrape booking.com using playwright

    **Request Body:**
    - `hotel_name` (str): The name of the hotel to search for.

    **Returns:**
        dict: A dictionary containing the hotel's name, address, description, and review score.
    """
    async with async_playwright() as p:
        page_url = BOOKING_URL + transform_search_name(hotel_name)

        LOG.debug(f"Scraping URL: {page_url}")
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(page_url, timeout=60000)

        url = await page.query_selector(
            'div[data-testid="property-card-container"] div div a'
        )

        if url is None:
            LOG.error("No property URL found on the page")
            raise ValueError("No URL found for the hotel")

        LOG.debug("Getting href attribute")
        href = await url.get_attribute("href")

        if href is None:
            LOG.error("The selected property does not have an href attribute")
            raise ValueError("URL does not have an href attribute")

        return await get_info(href)


@router.post("/api/hotels")
async def save(hotel: Hotel) -> Dict[str, Union[str, Hotel]]:
    """
    Save a hotel to the database.

    **Request Body:**
      - `hotel` (Hotel): The hotel object containing the details to be saved.

    **Returns:**
     - `dict`: A dictionary containing a success message and the saved hotel data.

    **Raises:**
        HTTPException: If an error occurs during the saving process,
            an HTTPException with status code 500 is raised.
    """
    LOG.debug("Saving hotel data")
    try:
        saved_hotel = crud.create_hotel(
            name=hotel.name,
            address=hotel.address,
            description="some description",
            review=hotel.review,
            db=crud.get_db(),
        )
        LOG.debug(f"Hotel data saved successfully: {saved_hotel}")
        return {"message": "Hotel data saved successfully", "hotel": saved_hotel}

    except Exception as exc:
        LOG.error(f"An error occurred while saving the hotel data: {str(exc)}")
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(exc)}"
        ) from exc


@router.get("/api/hotels")
async def get_hotels():
    """
    Get all hotels basic information.

    **Returns:**
        List[Hotel]: A list of hotel objects containing basic information.
    """
    db = crud.get_db()
    hotels = crud.get_hotels_basic_info(db)
    if hotels is None:
        raise HTTPException(status_code=404, detail="Hotels not found")

    return hotels


@router.get("/api/hotels/{id}/", response_model=Hotel)
async def get_hotel(id: int) -> Hotel:
    """
    Get a specific hotel by ID, including its details.

    **Request Body:**
        - `id` (int): The hotel ID to retrieve.

    **Returns:**
        Hotel: The hotel object containing the details.

    **Raises:**
        HTTPException: If the hotel is not found, an HTTPException with status code 404 is raised.
    """
    db = crud.get_db()
    hotel = crud.get_hotel_by_id(db=db, hotel_id=id)

    if hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")

    return hotel
