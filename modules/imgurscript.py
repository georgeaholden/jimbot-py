import requests
import os
import os.path
from dotenv import load_dotenv


def get_token():
    load_dotenv()
    token = os.getenv("IMGUR_ACCESS_TOKEN")
    return token


def upload(path):
    if os.path.isfile(path):
        pass
    elif os.path.isdir(path):
        pass
    else:
        print('Invalid path')


def never():
    files = {'video': open('../test.mp4', 'rb')}
    body = {'disable_audio': 1}
    r = requests.request('POST', 'https://api.imgur.com/3/upload',
                         headers={'Authorization': 'Bearer {}'.format(token)}, files=files, data=body)
    print(r.status_code)
    print(r.content)


def delete_all():
    print('Not currently implemented')


def main():
    token = get_token()

    print("Simple imgur gif/video uploading script")
    print("Type upload {filepath} to upload files")
    print("Type delete to remove all uploaded images")
    while True:
        command = input("Enter a command ")
        if command.lower().startswith('upload'):
            path = command.split()[1]
            upload(path)
        if command.lower().startswith('delete'):
            delete_all()


main()
