from typing import List, Set
import random
from logging import getLogger

from .models import Post
from .protocols import (
    ExternalAPIGateway,
    DataBaseGateway,
)


logger = getLogger(__name__)

class FetchDataFromApi:
    def __init__(
        self,
        external_api_gateway: ExternalAPIGateway,
        database_gateway: DataBaseGateway
    ):
        self.external_api_gateway = external_api_gateway
        self.database_gateway = database_gateway


    def __call__(self) -> None:
        offsets = self._generate_uniq_nums()
        for offset in offsets:
            logger.info(f'Offset: {offset}')
            data = self.external_api_gateway.fetch_data(offset)
            if data:
                self._process_save_data(data)
    
    def _generate_uniq_nums(self) -> Set[int]:
        generated_numbers = set()
        while len(generated_numbers) < 1000:
            num = random.randint(0, 1000)
            if num not in generated_numbers:
                generated_numbers.add(num)
        return generated_numbers

    def _process_save_data(self, data: List[Post]) -> None:
        posts_list_for_save = []
        for item in data:
            if not self.database_gateway.exists_by_body_and_payment_data(
                item.body,
                item.payment_data
            ):
                posts_list_for_save.append(item)
                logger.info(f'Post added to save')
        self.database_gateway.save_all_posts(posts_list_for_save)
