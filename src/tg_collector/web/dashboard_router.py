from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


router = APIRouter(tags=['Dashboard'])
templates = Jinja2Templates(directory='/static')

@router.get('/', response_class=HTMLResponse)
def render_dashboard():
    return templates.TemplateResponse('dashboard.html')
