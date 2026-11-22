from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

TEMPLATES = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))

router = APIRouter(tags=["pages"])


@router.get("/", response_class=HTMLResponse)
def student_page(request: Request):
    return TEMPLATES.TemplateResponse(request, "student.html", {})


@router.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request):
    return TEMPLATES.TemplateResponse(request, "admin.html", {})
