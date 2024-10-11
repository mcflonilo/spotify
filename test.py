import requests
#access token = BQDaf2rhT-fQXckLhOp6AMSS819y7ZgkG2K3geifp5hPDnjI9ZH_sirajhyysfMl_sV3h2eIhCAfhI8EEhdgRWVz5PzWQBNSggbhE_jDP__gLYdYhQs


def get_access_token():
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'client_id': 'f38377398eb14acdaf4366d72642faf9',
        'client_secret': 'd6d7a864ba7844b1b68a2f2e3ba5aebe'
}
    response = requests.post(url, headers=headers, data=data)
    return response.json().get('access_token')

access_token = get_access_token()
print(access_token)

url = "https://api.spotify.com/v1/me/top/artists"
headers = {"Authorization": "Bearer {}".format(access_token)}
response = requests.get(url, headers=headers)

print(response.status_code)
print(response.json())