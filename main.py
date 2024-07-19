import datetime
import logging
import time

import requests
from requests.auth import HTTPDigestAuth
import yaml

logger = logging.getLogger(__name__)


def get_time(endpoint, auth):
    uri = endpoint + "/cgi-bin/global.cgi?action=getCurrentTime"
    r = requests.get(uri, auth=auth, timeout=10)
    if r.status_code != 200:
        logging.error(f"Status Code for {uri}: {r.status_code}")

    else:
        logging.info(f"Camera time is: {(r.text).strip()}")


def get_locales(endpoint, auth):
    uri = endpoint + "/cgi-bin/configManager.cgi?action=getConfig&name=Locales"
    r = requests.get(uri, auth=auth, timeout=10)
    if r.status_code != 200:
        logging.error(f"Status Code for {uri}: {r.status_code}")
        logging.error(f"Reason: {r.reason}")

    else:
        logging.info(f"Camera time is: {(r.text).strip()}")


def set_time(endpoint, auth):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    uri = endpoint + "/cgi-bin/global.cgi?action=setCurrentTime&time=" + now
    r = requests.get(uri, auth=auth, timeout=10)
    if r.status_code != 200:
        logging.error(f"Status Code for {endpoint}: {r.status_code}")
    else:
        logging.info(f"Set {endpoint} to {now}")


def main():
    logging.basicConfig(level=logging.INFO)
    with open("config.yml", encoding="utf-8") as f:
        config = yaml.safe_load(f.read())

    auth = HTTPDigestAuth(config["api_user"], config["api_password"])

    # doorbell user is set to admin - I cannot change it
    doorbell_auth = HTTPDigestAuth("admin", config["api_password"])

    # don't need to sync doorbell but want it in here anyways
    print("remove doorbell config")
    endpoints = [x for x in config["endpoints"] if "doorbell" not in x]

    for endpoint in endpoints:
        # get_locales(endpoint, auth)
        get_time(endpoint, auth)
        set_time(endpoint, auth)
        get_time(endpoint, auth)


if __name__ == "__main__":
    main()
    # while True:
    #     main()
    #     time.sleep(300)
