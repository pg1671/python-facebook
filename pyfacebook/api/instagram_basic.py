"""
    Instagram Basic display Api impl
"""
from typing import Dict, Optional, Union, List, Tuple, Set

from pyfacebook.api.base import BaseApi
from pyfacebook.error import PyFacebookException, ErrorCode, ErrorMessage
from pyfacebook.models import AuthAccessToken, IgBasicUser, IgBasicMedia
from pyfacebook.utils import constant
from pyfacebook.utils.param_validation import enf_comma_separated


class IgBasicApi(BaseApi):
    GRAPH_URL = "https://graph.instagram.com/"
    DEFAULT_AUTHORIZATION_URL = "https://api.instagram.com/oauth/authorize"
    DEFAULT_EXCHANGE_ACCESS_TOKEN_URL = "https://api.instagram.com/oauth/access_token"

    DEFAULT_SCOPE = ["user_profile"]

    def __init__(self,
                 app_id=None,
                 app_secret=None,
                 short_token=None,
                 long_term_token=None,
                 initial_access_token=True,
                 timeout=None,  # type: Optional[int]
                 sleep_on_rate_limit=False,  # type: bool
                 proxies=None,  # type: Optional[dict]
                 debug_http=False  # type: bool
                 ):
        BaseApi.__init__(self,
                         app_id=app_id,
                         app_secret=app_secret,
                         short_token=short_token,
                         long_term_token=long_term_token,
                         timeout=timeout,
                         initial_access_token=initial_access_token,
                         sleep_on_rate_limit=sleep_on_rate_limit,
                         proxies=proxies,
                         debug_http=debug_http
                         )

    @staticmethod
    def _generate_secret_proof(secret, access_token):  # type: (str, str) -> Optional[str]
        return None

    def get_app_token(self, return_json=False):
        raise PyFacebookException(ErrorMessage(
            code=ErrorCode.NOT_SUPPORT_METHOD,
            message="Method not support by this api."
        ))

    def get_token_info(self, input_token=None, return_json=False):
        raise PyFacebookException(ErrorMessage(
            code=ErrorCode.NOT_SUPPORT_METHOD,
            message="Method not support by this api."
        ))

    def exchange_insights_token(self, page_id, access_token=None):
        raise PyFacebookException(ErrorMessage(
            code=ErrorCode.NOT_SUPPORT_METHOD,
            message="Method not support by this api."
        ))

    def get_long_token(self, short_token, app_id=None, app_secret=None, return_json=False):
        # type: (str, Optional[str], Optional[str], bool) -> Optional[Union[AuthAccessToken, Dict]]
        """
        Exchange a short-lived Instagram User Access Token for a long-lived Instagram User Access Token.

        :param short_token: short-lived Instagram User Access Token.
        :param app_id: Your Instagram app's id, this not necessary.
        :param app_secret: Your Instagram app's secret.
        :param return_json: Set to false will return instance of AuthAccessToken.
        Or return json data. Default is false.
        :return: Access token data.
        """
        if app_secret is None:
            app_secret = self.app_secret

        resp = self._request(
            path="access_token",
            args={
                "grant_type": "ig_exchange_token",
                "client_secret": app_secret,
                "access_token": short_token,
            },
            enforce_auth=False
        )
        data = self._parse_response(resp)

        if return_json:
            return data
        else:
            return AuthAccessToken.new_from_json_dict(data)

    def refresh_access_token(self, access_token=None, return_json=False):
        # type: (Optional[str], bool) -> Optional[Union[AuthAccessToken, Dict]]
        """
        :param access_token: long-lived token will be refreshed.
        :param return_json: Set to false will return instance of AuthAccessToken.
        Or return json data. Default is false.
        :return: New long-lived access token data
        """
        if access_token is None:
            access_token = self._access_token

        resp = self._request(
            path="refresh_access_token",
            args={
                "grant_type": "ig_refresh_token",
                "access_token": access_token
            }
        )
        data = self._parse_response(resp)

        if return_json:
            return data
        else:
            return AuthAccessToken.new_from_json_dict(data)

    def get_user_info(self, user_id=None, fields=None, return_json=False):
        # type: (str, Optional[Union[str, List, Tuple, Set]], bool) -> Union[IgBasicUser, Dict]
        """
        Retrieve user basic info for target user.
        :param user_id: The id for you want to get data. If not provide, will use access token belong user
        :param fields: Comma-separated id string for data fields which you want.
                You can also pass this with an id list, tuple, set.
        :param return_json: Set to false will return a list instance of IgBasicUser.
                Or return json data. Default is false.
        :return: User info data
        """

        if user_id is None:
            user_id = "me"

        if fields is None:
            fields = constant.INSTAGRAM_BASIC_USER_FIELD

        args = {
            "fields": enf_comma_separated(field="fields", value=fields)
        }

        resp = self._request(
            path="{}".format(user_id),
            args=args
        )
        data = self._parse_response(resp)

        if return_json:
            return data
        else:
            return IgBasicUser.new_from_json_dict(data)
