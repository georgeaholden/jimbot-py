"""Super basic python script that uploads or deletes imgur files and prints the uploaded urls"""


import requests
import os
import os.path
from dotenv import load_dotenv
import json

CONTENT_TYPE = {'jpg': 'image', 'png': 'image', 'mp4': 'video', 'mpeg': 'video'}


def get_token():
    load_dotenv()
    token = os.getenv("IMGUR_ACCESS_TOKEN")
    return token


def upload(token, path):
    if os.path.isfile(path):
        _, suffix = path.split('.')
        content = {CONTENT_TYPE[suffix]: open(path, 'rb')}
        body = {'disable_audio': 1}
        r = requests.request('POST', 'https://api.imgur.com/3/upload',
                             headers={'Authorization': 'Bearer {}'.format(token)}, files=content, data=body)
        body = json.loads(r.text)
        print('https://imgur.com/' + body['data']['id'])
    elif os.path.isdir(path):
        filenames = os.listdir(path)
        urls = []
        for filename in filenames:
            _, suffix = filename.split('.')
            content = {CONTENT_TYPE[suffix]: open(path + '/' + filename, 'rb')}
            body = {'disable_audio': 1}
            if r.status_code == 200:
                r = requests.request('POST', 'https://api.imgur.com/3/upload',
                                     headers={'Authorization': 'Bearer {}'.format(token)}, files=content, data=body)
                body = json.loads(r.text)
                urls.append('https://imgur.com/' + body['data']['id'])
            else:
                print('file: {} failed to upload'.format(filename))
                print(r.status_code)
        print(urls)
    else:
        print('Invalid path')


def never():
    files = {'video': open('../test.mp4', 'rb')}
    body = {'disable_audio': 1}
    r = requests.request('POST', 'https://api.imgur.com/3/upload',
                         headers={'Authorization': 'Bearer {}'.format(token)}, files=files, data=body)
    print(r.status_code)
    print(r.content)


def delete_all(token):
    r = requests.request('GET', 'https://api.imgur.com/3/account/me/images',
                         headers={'Authorization': 'Bearer {}'.format(token)})
    delete_hashes = []
    body = json.loads(r.text)
    for entry in body['data']:
        delete_hashes.append(entry['deletehash'])

    for target in delete_hashes:
        r = requests.request('DELETE', 'https://api.imgur.com/3/image/{}'.format(target),
                             headers={'Authorization': 'Bearer {}'.format(token)})
        print(r.status_code)


def main():
    token = get_token()
    print("Simple imgur gif/video uploading script")
    print("Type upload {filepath} to upload files")
    print("Type delete to remove all uploaded images")
    while True:
        command = input("Enter a command ")
        if command.lower().startswith('upload'):
            path = command.split()[1]
            upload(token, path)
        elif command.lower().startswith('delete'):
            delete_all(token)
        else:
            print('Unrecognised command')


main()
