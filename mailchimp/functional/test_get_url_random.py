import os
import sys
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from filibuster.assertions import was_fault_injected

examples_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(examples_path)
import helper
helper = helper.Helper("mailchimp")

s = requests.Session()

def test_functional_get_url_random():
    random_url = "randomurl"
    response = s.get("http://{}:{}/urls/{}".format(helper.resolve_requests_host('load-balancer'),
            helper.get_port('load-balancer'), random_url), timeout=helper.get_timeout('load-balancer'))
    
    try:
        if not was_fault_injected():
            assert response.status_code == 200
            assert response.json() == {"result": random_url}
        else:
            # Incorrect failure handling by the app-server.
            if response.status_code == 503:
                assert True
            # Fallback triggered.
            elif response.status_code == 200:
                assert response.json()["result"] == random_url
            else:
                assert False
    except AssertionError as e:
        print("Response Headers:", response.headers)
        print("Response Body:", response.text)
        raise e


if __name__ == '__main__':
    try:
        test_functional_get_url_random()
    finally:
        s.close()
