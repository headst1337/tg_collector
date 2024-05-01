from datetime import datetime

from sqlalchemy import Integer, String, Column, MetaData, Table, DateTime
from sqlalchemy.orm import registry

from tg_collector.application.models import Post


metadata_obj = MetaData()
mapper_registry = registry()

post = Table(
    'posts',
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('post_link', String(128)),
    Column('group_link', String(128)),
    Column('body', String(1024)),
    Column('payment_data', String(1024)),
    Column('timestamp', DateTime, default=datetime.now)
)

mapper_registry.map_imperatively(Post, post)
