from http import HTTPStatus

import pytest
from mcp.server.fastmcp.exceptions import ToolError
from spotantic.models import ErrorResponseModel
from spotantic.types.exceptions import SpotanticException
from spotantic.types.exceptions import SpotanticInvalidResponseError
from spotantic.types.exceptions import SpotanticResponseError
from spotantic.types.exceptions import SpotanticTooManyRequests

from spotantic_mcp.tools.endpoints._handle_endpoint_errors import handle_spotantic_errors
from spotantic_mcp.tools.endpoints._views import SimplifiedAlbumView


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "exception",
    [
        SpotanticResponseError(
            ErrorResponseModel(status=HTTPStatus.INTERNAL_SERVER_ERROR, message="Internal server error")
        ),
        SpotanticTooManyRequests(ErrorResponseModel(status=HTTPStatus.TOO_MANY_REQUESTS, message="Too many requests")),
        SpotanticInvalidResponseError("Invalid response format"),
        SpotanticException("General error"),
    ],
)
async def test_handle_spotantic_errors(exception):
    @handle_spotantic_errors
    async def dummy_tool():
        raise exception

    with pytest.raises(ToolError) as exc_info:
        await dummy_tool()
        assert str(exc_info.value) == (
            f"Spotify API call failed! Exception class name: {exception.__class__.__name__}, message: {str(exception)}"
        )


@pytest.mark.asyncio
async def test_handle_spotantic_errors_validation_error():
    @handle_spotantic_errors
    async def dummy_tool():
        SimplifiedAlbumView(
            album_type="album",  # type: ignore
            id=123,  # type: ignore
            name="Test Album",
            release_date="2023-01-01",  # type: ignore
            total_tracks=10,
        )

    with pytest.raises(ToolError, match="Data validation failed! Exception message:"):
        await dummy_tool()
