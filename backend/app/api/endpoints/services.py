"""This module provides services for scraping hotel information from web pages using Playwright."""

from typing import Any, Dict, Optional, Union

from app.api.endpoints.logger import setup_logger
from playwright.async_api import Page, async_playwright
from pydantic import BaseModel

LOG = setup_logger("ta-ast-services")


DATA = {
    "name": 'div[id="hp_hotel_name"] div h2',
    "address": "#wrap-hotelpage-top > div:nth-child(4) > div > div > span.f419a93f12 > div",
    "description": "#basiclayout > div.hotelchars > div.page-section.hp--desc_highlights.js-k2-hp--block >  div > div.bui-grid__column.bui-grid__column-8.k2-hp--description > div.hp-description > div.hp_desc_main_content > div > div > p.a53cbfa6de.b3efd73f69",
    "review": 'div[data-testid="review-score-right-component"] div',
}


class Hotel(BaseModel):
    """
    Hotel model representing a hotel entity.

    **Request Body:**
     - `name` (str): The name of the hotel.
     - `address` (str): The address of the hotel.
     - `description` (Optional[str]): A brief description of the hotel.
     - `review` (float): The review rating of the hotel.
    """

    name: str
    address: str
    description: str
    review: float


def transform_search_name(name: str) -> str:
    """
    Transforms the given search name by replacing spaces with '+' and converting to lowercase.

    **Request Body:**
        - `name` (str): The search name to be transformed.
    **Returns:**
        str: The transformed search name.
    """
    if name:
        return name.replace(" ", "+").lower()
    else:
        raise ValueError("Invalid search name")


async def get_text_content(page: Page, selector: str) -> Optional[str]:
    """
    Get the text content of an element identified by the given selector.

    **Request Body:**
        - `page` (playwright.async_api.Page): The Playwright page object.
        - `selector` (str): The selector to identify the element.

    **Returns:**
        str: The text content of the element.
    """
    LOG.debug(f"Getting text content for selector: {selector}")
    review = await page.query_selector(selector)

    if review:
        text_content = await review.text_content()
        LOG.debug(f"Found review element: {text_content}")
        return text_content
    else:
        LOG.error(f"No review element found for selector: {selector}")
        return None


async def get_data(page: Page, data: Dict[Any, Any] = DATA) -> None:
    """
    Get the text content of elements identified by the given selectors
    and assign them to global variables.

    **Request Body:**
        - `page` (playwright.async_api.Page): The Playwright page object.
        - `data` (dict): A dictionary containing the element selectors.

    """
    for key, value in data.items():
        globals()[key] = await get_text_content(page, value)


async def get_info(page_url: str) -> Dict[str, Union[str, float, None]]:
    """
    Fetch hotel information from the given page URL.

    **Request Body:**
    - `page_url` (str): The URL of the hotel page to scrape.

    **Returns:**
        dict: A dictionary containing the hotel's name, address, description, and review score.

    **Example Request:**
        {
            "name": "Hotel Example",
            "address": "123 Example Street, Example City",
            "description": "This is an example description of the hotel.",
            "review": "8.5"
        }
    """
    LOG.debug(f"Scraping URL: {page_url}")
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(page_url, timeout=60000)

        LOG.debug("Getting hotel information")

        # Get hotel informations defined in DATA
        await get_data(page)

        LOG.info("Hotel information: ")
        for k in DATA.keys():
            LOG.info(f"{k}: {globals()[k]}")

        return {
            "name": globals().get("name"),
            "address": globals().get("address"),
            "description": globals().get("description"),
            "review": convert_comma_to_dot(globals().get("review", "").split()[-1]),
        }


def convert_comma_to_dot(number_str: str) -> float:
    """
    Converts a number string with a comma as the decimal separator to a float.

    **Request Body:**
        - `number_str` (str): The number string to convert.

    **Returns:**
        The converted float number.

    **Raises:**
        ValueError: If the number string is not in a valid format.
    """
    try:
        return float(number_str.replace(",", "."))
    except ValueError as exc:
        LOG.error(f"Invalid number format: {number_str}")
        raise ValueError(f"Invalid number format: {number_str}") from exc
