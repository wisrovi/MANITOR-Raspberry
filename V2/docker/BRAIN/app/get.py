import requests


def get(url):
    try:
        r = requests.get(url=url)
        data = r.json()
        return data
    except Exception as err:
        # print(err)
        print(url)
        return None
