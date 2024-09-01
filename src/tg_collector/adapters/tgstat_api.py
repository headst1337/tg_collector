import os
import re
from urllib.parse import urlencode

import requests

from tg_collector.application.protocols import TGStatAPIGateway
from tg_collector.application.models import Post


class TGStatSearchAPI(TGStatAPIGateway):
    def __ini__(self) -> None:
        self.api_url = 'https://api.tgstat.ru/posts/search'
        self.token = os.getenv('TGSTAT_TOKEN')
        self.prompt = os.getenv('PROMPT')

    def fetch_data(self, offset: int) -> list[Post | None]:
        url = self._build_url(offset)
        response = requests.get(url)
        if response.status_code == 200:
            parsed_data = self._process_parse_data(response.json())
            if parsed_data:
                return parsed_data
        return [None]

    def _build_url(self, offset: int) -> str:
        query_params = {
            'token': self.token,
            'q': self.prompt,
            'extended': 1,
            'offset': offset,
            'limit': 50,
            'country': 'ua',
            'language': 'ukrainian',
            'hideForwards': 1,
            'extendedSyntax': 1
        }
        return self.api_url + '?' + urlencode(query_params)

    def _process_parse_data(self, data: dict) -> list[Post | None]:
        posts: list[Post | None] = []
        if 'response' in data and 'items' in data['response']:
            for item in data['response']['items']:
                post_link = item['link']
                group_link: str = next(
                    (
                        channel['link']
                        for channel in data['response']['channels']
                        if channel['id'] == item['channel_id']
                    ),
                    'not found'
                )
                body = item['text']
                payment_data = self._extract_filtered_data(item['text'])
                if payment_data:
                    timestamp = item['date']
                    post = Post(
                        post_link=post_link,
                        group_link=group_link,
                        body=body,
                        payment_data=payment_data,
                        timestamp=timestamp
                    )
                    posts.append(post)
                else:
                    # logger.warning("No payment data")
                    pass
        return posts

    def _extract_filtered_data(self, text: str) -> str | None:
        crypto_pattern = r'(0x[a-fA-F0-9]{40}|[13][a-km-zA-HJ-NP-Z0-9]{26,35})'
        mono_link_pattern = r'https://send\.monobank\.ua/jar/[a-zA-Z0-9]+'
        card_pattern = r'(\d{4}\s?\d{4}\s?\d{4}\s?\d{4})|(\d{16})'

        patterns = [crypto_pattern, mono_link_pattern, card_pattern]
        result_data: list = []

        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                for match in matches:
                    if isinstance(match, tuple):
                        result_data.extend(match)
                    else:
                        result_data.append(match)

        return '\n'.join(list(dict.fromkeys(result_data))) if result_data else None
