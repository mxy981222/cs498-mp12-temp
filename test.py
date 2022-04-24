import requests
import json
url = "https://seorwrpmwh.execute-api.us-east-1.amazonaws.com/prod/mp12-grader"
payload = {
            "accountId": 455277168335,
            "submitterEmail": 'xingyum2@illinois.edu',
            "secret": 's6VcdAnYX59DTMdR',
            "ipaddress": '3.235.17.116:5000'
    }
r = requests.post(url, data=json.dumps(payload))
print(r.status_code, r.reason)
print(r.text)