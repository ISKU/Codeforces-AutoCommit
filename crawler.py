import sys
import requests
from bs4 import BeautifulSoup

USER_STATUS_URL = 'http://codeforces.com/api/user.status?'
SUBMISSION_URL_FORMAT = 'http://codeforces.com/contest/%d/submission/%d'
ERROR_FORMAT = '* Error: %s'

class Crawler:

    def get_user_status(self, handle, start=0, offset=0):
        params = {'handle' : handle}
        if (not start == 0) or (not offset == 0):
            params['from'] = start
            params['count'] = offset

        res = requests.get(USER_STATUS_URL, params)

        if res.status_code == 400:
            sys.exit(ERROR_FORMAT % ('get_user_status, ' + res.json()['comment']))
        if res.status_code == 200:
            return res.json()['result']

        sys.exit(ERROR_FORMAT % ('get_user_status, ' + res.status_code))

    def get_source(self, submission_id, contest_id):
        res = requests.get(SUBMISSION_URL_FORMAT % (contest_id, submission_id))

        if not res.status_code == 200:
            sys.exit(ERROR_FORMAT % ('get_source, ' + res.status_code))

        soup = BeautifulSoup(res.text, 'html.parser')
        source = soup.find(id='program-source-text')

        if source is None:
            return True, None
        return False, source.get_text()
