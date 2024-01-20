from dotenv import load_dotenv
import argparse
import os
import requests
from urllib.parse import urlparse


def shorten_link(token, link):
    url = 'https://api-ssl.bitly.com/v4/shorten'
    params = {"long_url": link}
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, headers=headers, json=params)
    response.raise_for_status()
    return response.json()['id']


def count_clicks(token, bitlink):
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    params = {"unit": "month", "units": -1}
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(token, bitlink):
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    token = os.environ['BITLY_TOKEN']
    parser = argparse.ArgumentParser(description='Эта программа умеет сокращать ссылки, а также считать сумму кликов по уже сокращенной ссылке')
    parser.add_argument('--url', type=str, help='Введите ссылку')
    args = parser.parse_args()
    parsed_url=urlparse(args.url)
    parsed_url=f"{parsed_url.netloc}{parsed_url.path}"
    try:
        if is_bitlink(token, parsed_url):
            print("Сумма кликов: ", count_clicks(token, parsed_url))
        else:
            print(shorten_link(token, args.url))
    except requests.exceptions.HTTPError:
        print("Ошибка, проверьте ссылку.")


if __name__ == "__main__":
    main()
