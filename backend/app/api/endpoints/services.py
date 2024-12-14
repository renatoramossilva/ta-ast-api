"""This module provides services for scraping hotel information from web pages using Playwright."""

from typing import Dict, Optional, Union

from playwright.async_api import async_playwright
from pydantic import BaseModel


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
    description: Optional[str]
    review: float


def transform_search_name(name: str) -> str:
    """
    Transforms the given search name by replacing spaces with '+' and converting to lowercase.

    **Request Body:**
        - `name` (str): The search name to be transformed.
    **Returns:**
        str: The transformed search name.
    """
    return name.replace(" ", "+").lower()


async def get_info(page_url: str) -> Dict[str, Union[str, float]]:
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
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(page_url, timeout=60000)

        name = await page.query_selector('div[id="hp_hotel_name"] div h2')
        address = await page.query_selector(
            "#wrap-hotelpage-top > div:nth-child(4) > div > div > span.f419a93f12 > div"
        )
        description = await page.query_selector(  # pylint: disable=unused-variable
            "#basiclayout > div.hotelchars > "
            "div.page-section.hp--desc_highlights.js-k2-hp--block >  div > "
            "div.bui-grid__column.bui-grid__column-8.k2-hp--description > div.hp-description > "
            "div.hp_desc_main_content > div > div > p.a53cbfa6de.b3efd73f69"
        )
        review = await page.query_selector(
            'div[data-testid="review-score-right-component"] div'
        )
        rev = await review.text_content()

        return {
            "name": await name.text_content(),
            "address": await address.text_content(),
            "description": "some_desc",  # await description.text_content(),
            "review": convert_comma_to_dot(rev.split()[-1]),
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
        raise ValueError(f"Invalid number format: {number_str}") from exc
