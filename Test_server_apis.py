import requests
import json

url = "http://35.222.60.164"
ID = "gondola8"
url = "{}/api/stand_status/{}".format(url,ID)
payload = {
    'Data': [
    {'ID': 1, 'Name': 'shelf_0_camera', 'file': 'shelf_0_camera.jpg', 'file_AI': 'shelf_0_camera_AI.jpg', 'total_bottles': 0, 'Status': True},
    {'ID': 2, 'Name': 'shelf_1_camera', 'file': 'shelf_1_camera.jpg', 'file_AI': 'shelf_1_camera_AI.jpg', 'total_bottles': 0, 'Status': True},
    {'ID': 3, 'Name': 'shelf_2_camera', 'file': 'shelf_2_camera.jpg', 'file_AI': 'shelf_2_camera_AI.jpg', 'total_bottles': 0, 'Status': True},
    {'ID': 4, 'Name': 'shelf_3_camera', 'file': 'shelf_3_camera.jpg', 'file_AI': 'shelf_3_camera_AI.jpg', 'total_bottles': 0, 'Status': True},
    {'ID': 5, 'Name': 'shelf_4_camera', 'file': 'shelf_4_camera.jpg', 'file_AI': 'shelf_4_camera_AI.jpg', 'total_bottles': 0, 'Status': True}
    ]
}
payload = json.dumps(payload)
print(payload)
headers = {'Content-Type': 'application/json'}
response = requests.request("POST", url, headers=headers, data=payload)
print(response)