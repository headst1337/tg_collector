from dataclasses import dataclass, field


@dataclass
class Post():
    id: int = field(init=False)
    post_link: str
    group_link: str
    body: str
    payment_data: str
    timestamp: float
