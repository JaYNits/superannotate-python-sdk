import logging

from ..api import API
from ..exceptions import SABaseException

logger = logging.getLogger("superannotate-python-sdk")

_api = API.get_instance()


def search_users(team):
    """Search for users in team
    Returns
    -------
    list:
        list of of users
    """
    result_list = []
    team_id = team["id"]
    params = {'team_id': team_id, 'offset': 0}
    while True:
        response = _api.gen_request(
            req_type='GET', path='/users', params=params
        )
        if response.ok:
            res = response.json()
            result_list += res["data"]
            new_len = len(result_list)
            if res["count"] <= new_len:
                break
            params["offset"] = new_len
        else:
            raise SABaseException(
                response.status_code,
                "Couldn't search projects. " + response.text
            )

    return result_list
