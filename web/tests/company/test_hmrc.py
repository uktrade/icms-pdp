from unittest.mock import Mock, patch

import pytest

from web.company.hmrc import CompaniesHouseException, api


@patch("web.company.hmrc.requests.get")
def test_api_raise_error(_):
    """Raise an error when status code is not 200."""
    with pytest.raises(CompaniesHouseException):
        api("hello")


@patch("web.company.hmrc.requests.get")
def test_api_ok(mock_get):
    response = Mock()
    response.status_code = 200
    response.json.return_value = {"some_matched": "companies"}
    mock_get.return_value = response

    assert {"some_matched": "companies"} == api(query="my_search_request")
