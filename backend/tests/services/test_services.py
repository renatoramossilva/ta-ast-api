import pytest
from app.api.endpoints.services import (
    convert_comma_to_dot,
    get_data,
    get_text_content,
    transform_search_name,
)
from playwright.async_api import Page


@pytest.mark.parametrize(
    "input_str,expected_output,expected_error",
    [
        (
            "John Doe",
            "john+doe",
            False,
        ),
        (
            "",
            None,
            True,
        ),
        (
            None,
            None,
            True,
        ),
        (
            "John",
            "john",
            False,
        ),
        (
            "John    Doe",
            "john++++doe",
            False,
        ),
    ],
)
def test_transform_search_name(input_str, expected_output, expected_error):
    if expected_error:
        with pytest.raises(ValueError, match="Invalid search name"):
            transform_search_name(input_str)
    else:
        assert transform_search_name(input_str) == expected_output


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "return_value",
    [
        ("This is a review"),
        (None),
        # (""),
    ],
)
async def test_get_text_content_found(mocker, return_value):
    mock_element = mocker.AsyncMock()
    mock_element.text_content.return_value = return_value

    mock_page = mocker.Mock(spec=Page)
    mock_page.query_selector = mocker.AsyncMock(return_value=mock_element)

    result = await get_text_content(mock_page, "#review")

    mock_page.query_selector.assert_called_once_with("#review")
    mock_element.text_content.assert_called_once()
    assert result == return_value


@pytest.mark.parametrize(
    "number_str,expected_output,expected_error",
    [
        (
            "1,23",
            1.23,
            False,
        ),
        (
            "20,34",
            20.34,
            False,
        ),
        (
            "3,4",
            3.4,
            False,
        ),
        (
            "1234",
            1234.0,
            False,
        ),
        (
            "0",
            0.0,
            False,
        ),
        (
            "999999,9999",
            999999.9999,
            False,
        ),
        (
            "",
            None,
            True,
        ),
    ],
)
def test_convert_comma_to_dot(number_str, expected_output, expected_error):
    if expected_error:
        with pytest.raises(ValueError, match="Invalid number format"):
            convert_comma_to_dot(number_str)
    else:
        assert convert_comma_to_dot(number_str) == expected_output
