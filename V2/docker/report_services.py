ip = "localhost"

URLS = list()
URLS.append('http://{0}:5001/help'.format(ip))
URLS.append('http://{0}:5002/help'.format(ip))
URLS.append('http://{0}:5003/help'.format(ip))
URLS.append('http://{0}:5004/help'.format(ip))
URLS.append('http://{0}:5005/help'.format(ip))
URLS.append('http://{0}:5006/help'.format(ip))
URLS.append('http://{0}:5007/help'.format(ip))

import requests


def get(url_send_get):
    try:
        r = requests.get(url=url_send_get)
        data = r.json()
        return data
    except Exception as err:
        # print(err)
        print(url_send_get)
        return None


if __name__ == '__main__':
    responses = list()
    for url in URLS:
        rta = get(url)
        responses.append(rta)

    print("report:")
    for i, v in enumerate(URLS):
        print(v, responses[i])
