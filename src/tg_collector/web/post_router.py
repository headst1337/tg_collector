from typing import Annotated
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse

from tg_collector.adapters.sqlalchemy_db.repository import PostRepository
from tg_collector.adapters.generate_exel_report import GenerateExelReport
from tg_collector.adapters.tgstat_api import TGStatSearchAPI
from tg_collector.application.parse import FetchDataFromApi

from .schemas import DateRequest


router = APIRouter(tags=['Post'])


@router.get('/api/v1/post/get')
async def get_posts(
    date: str,
    post_repository: Annotated[PostRepository, Depends()],
):
    try:
        date = datetime.strptime(date, '%d-%m-%Y').date()
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail='Incorrect date format, should be dd-mm-yyyy'
        )
    posts = post_repository.get_by_date(date)
    posts_count = len(posts)
    return {'posts': post_repository.get_by_date(date), 'count': posts_count}


@router.get('/api/v1/post/available_dates')
async def check_post_availability(
    post_repository: Annotated[PostRepository, Depends()],
):
    return {'uniq_dates': post_repository.get_unique_dates()}


@router.post('/api/v1/post/download')
async def download_posts(
    request: DateRequest,
    exel_report: Annotated[GenerateExelReport, Depends()]
):
    report_file = exel_report.genetare_report(request.dates)
    return FileResponse(
        report_file,
        filename='report.xlsx',
        media_type='application/vnd.openxmlformats-officedocument.\
            spreadsheetml.sheet'
    )


@router.post('/api/v1/post/fetch')
async def fetch_data():
    fetcher = FetchDataFromApi(TGStatSearchAPI, PostRepository)
    fetcher.process_fetch()
    return {'status': 'success'}
