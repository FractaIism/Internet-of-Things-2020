# API module for communicating with MediaTek Cloud Sandbox
# Only post_mcs() and get_mcs() are meant to be used
# post_to_mcs() and get_from_mcs() use http.client and are deprecated in favor of the above functions which utilize the requests module
# The other functions are for internal operations

import json, http.client, requests, time, socket, random

deviceId = 'DP6Oqim8'
deviceKey = 'UvyvFY9TAm8VgVOt'

def post_mcs(data_channel, value):
    payload = make_payload(data_channel, value)
    headers = {
        "Content-type": "application/json",
        "deviceKey"   : deviceKey
    }
    url = f"http://api.mediatek.com/mcs/v2/devices/{deviceId}/datapoints"
    response = requests.post(url = url, headers = headers, data = json.dumps(payload))
    # one-liner response
    print(response.text)  # pretty-print response  # print(json.dumps(response.json(), indent = 4))

def get_mcs(data_channel):
    headers = {
        "deviceKey": deviceKey
    }
    url = f"http://api.mediatek.com/mcs/v2/devices/{deviceId}/datachannels/{data_channel}/datapoints"
    response = requests.get(url = url, headers = headers)
    # one-liner response
    print(response.text)
    # pretty-print response
    # print(json.dumps(response.json(), indent = 4))
    value = response.json()["dataChannels"][0]["dataPoints"][0]["values"]["value"]
    return value

# DEPRECATED! No longer used
# connect to MCS and return HTTP connection object
def connect_mcs():
    while True:
        try:
            conn = http.client.HTTPConnection("api.mediatek.com:80")
            conn.connect()
            return conn
        except (http.client.HTTPException, socket.error) as ex:
            print("Error: %s" % ex)
            time.sleep(10)

# DEPRECATED! Use post_mcs() instead
# update data in cloud
def post_to_mcs(data_channel, value):
    payload = make_payload(data_channel, value)
    headers = {
        "Content-type": "application/json",
        "deviceKey"   : deviceKey
    }
    conn = connect_mcs()
    conn.request(method = "POST", url = f"/mcs/v2/devices/{deviceId}/datapoints", body = json.dumps(payload),
                 headers = headers)
    response = conn.getresponse()
    # from sample code
    # print(response.status, response.reason, json.dumps(payload), time.strftime("%c"))
    response_payload = json.loads(response.read().decode())
    # one-liner response
    print(response_payload)
    # pretty-print response
    # print(json.dumps(response_payload, indent = 4))
    return

# DEPRECATED! Use get_mcs() instead
# retrieve data from cloud
def get_from_mcs(data_channel):
    headers = {
        "deviceKey": deviceKey
    }
    conn = connect_mcs()
    conn.request(method = "GET", url = f"/mcs/v2/devices/{deviceId}/datachannels/{data_channel}/datapoints",
                 headers = headers)
    response = conn.getresponse()
    response_payload = json.loads(response.read().decode())
    # one-liner response
    print(response_payload)
    # pretty-print response
    # print(json.dumps(response_payload, indent = 4))
    return response_payload["dataChannels"][0]["dataPoints"][0]["values"]["value"]

# make payload for MCS POST request
def make_payload(data_channel, value):
    payload = {
        "datapoints": [{
            "dataChnId": data_channel,
            "values"   : {
                "value": value
            }
        }]
    }
    return payload

# for testing the module
if __name__ == '__main__':
    # using http.client module (deprecated)
    while False:
        print()
        myfloat = random.random()
        # print("rand = %f" % myfloat)
        print("Posting to MCS ...")
        post_to_mcs('display', myfloat)
        print("Getting from MCS ...")
        val = get_from_mcs('control')
        print("control: ", val)
        time.sleep(3)
    # using requests module
    while True:
        print()
        print("Posting to MCS ...")
        post_mcs('display', random.random())
        print("Getting from MCS ...")
        datapoint = get_mcs('control')
        print("datapoint=", datapoint)
        time.sleep(3)
