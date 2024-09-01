from typing import List
from datetime import date

from sqlalchemy import func

from tg_collector.application.protocols import PostGateway
from tg_collector.application.models import Post
from tg_collector.main.dependencies import new_session


class PostRepository(PostGateway):
    def __init__(self) -> None:
        self.session = next(new_session())

    def save_all(self, posts: List[Post]) -> None:
        self.session.add_all(posts)
        self.session.commit()

    def get_all(self) -> List[Post]:
        return self.session.query(Post).all()

    def get_by_date(self, date: date) -> List[Post]:
        return self.session.query(Post).filter(
            func.DATE(Post.timestamp) == date
        ).all()

    def exists_by_body_and_payment_data(
            self,
            body: str,
            payment_data: str
    ) -> bool:
        return self.session.query(Post).filter(
            Post.body == body,
            Post.payment_data == payment_data
        ).first() is not None

    def get_unique_dates(self) -> List[str]:
        unique_dates = self.session.query(
            func.DATE(Post.timestamp)
        ).distinct().all()
        unique_dates_str = [
            date[0].strftime("%d-%m-%Y") for date in unique_dates
        ]
        return unique_dates_str
