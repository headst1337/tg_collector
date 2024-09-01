import random

from tg_collector.application.models import Post
from tg_collector.application.protocols import (
    TGStatAPIGateway,
    PostGateway,
)


class FetchDataFromApi:
    def __init__(
        self,
        external_api_gateway: TGStatAPIGateway,
        database_gateway: PostGateway
    ):
        self.external_api_gateway = external_api_gateway()
        self.database_gateway = database_gateway()

    def process_fetch(self) -> None:
        offsets = self._generate_uniq_nums()
        for offset in offsets:
            # logger.info(f'Offset: {offset}')
            if data := self.external_api_gateway.fetch_data(offset=offset):
                self._process_save_data(data)

    def _generate_uniq_nums(self) -> set[int]:
        generated_numbers: set = set()
        while len(generated_numbers) < 1000:
            num = random.randint(0, 1000)
            if num not in generated_numbers:
                generated_numbers.add(num)
        return generated_numbers

    def _process_save_data(self, data: list[Post]) -> None:
        posts_list_for_save = []
        for item in data:
            if not self.database_gateway.exists_by_body_and_payment_data(
                item.body,
                item.payment_data
            ):
                posts_list_for_save.append(item)
                # logger.info(f'Post added to save')
        self.database_gateway.save_all_posts(posts_list_for_save)
