import sys
import requests
from bs4 import BeautifulSoup

USER_STATUS_URL = 'http://codeforces.com/api/user.status?'
SUBMISSION_URL_FORMAT = 'http://codeforces.com/contest/%d/submission/%d'

class Crawler:

    def get_user_status(self, handle, start=0, offset=0):
        params = {'handle' : handle}
        if (not start == 0) or (not offset == 0):
            params['from'] = start
            params['count'] = offset

        res = requests.get(USER_STATUS_URL, params)

        if res.status_code == 400:
            return True, res.json()['comment']
        if res.status_code == 200:
            return False, res.json()['result']

        return True, str(res.status_code)

    def get_source(self, submission_id, contest_id):
        res = requests.get(SUBMISSION_URL_FORMAT % (contest_id, submission_id))

        if not res.status_code == 200:
            return True, str(res.status_code)

        soup = BeautifulSoup(res.text, 'html.parser')
        source = soup.find(id='program-source-text')

        if source is None:
            return True, 'faild to parse source'
        return False, source.get_text()
