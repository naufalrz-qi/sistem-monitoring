from flask_login import UserMixin
from ..lib.base_url import base_url
import requests as req

class UserLogin(UserMixin):
    # url = base_url + 'api/v2/auth/get-all'
    # resp = req.get(url)
    # jsonResp = resp.json()
    # data = []
    # for i in jsonResp:
    #     data.append({'id', i['id']})
    id = None

    