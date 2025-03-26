from fastapi import FastAPI
from backend.routers import test_employee  # Մեր փորձնական router-ը
from backend.routers import video_router
from backend.routers import workscore_router
from backend.routers import warehouse_router



app = FastAPI(
    title="WorkScore.ai API",
    description="Test API for Employee Schemas",
    version="0.1.0"
)

# Միացնում ենք router-ը
app.include_router(test_employee.router)

from backend.routers import employee_router
app.include_router(employee_router.router)

app.include_router(video_router.router)
app.include_router(workscore_router.router)
app.include_router(warehouse_router.router)



