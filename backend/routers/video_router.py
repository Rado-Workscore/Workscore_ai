from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List

from backend.schemas.video import VideoCreate, VideoOut
from backend.auth.dependencies import get_current_user, TokenData
from backend.services.video_service import create_video, get_videos_by_warehouse

router = APIRouter(
    prefix="/videos",
    tags=["Videos"]
)

# 🟢 Վիդեո վերբեռնում
@router.post("/upload", response_model=VideoOut)
def upload_video(
    data: VideoCreate,
    current_user: TokenData = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Միայն ադմինը կարող է վիդեո վերբեռնել։")

    return create_video(data)

# 🔵 Վիդեոների բերում ըստ պահեստի
@router.get("/", response_model=List[VideoOut])
def get_videos(
    warehouse_id: int = Query(..., description="Պահեստի ID"),
    current_user: TokenData = Depends(get_current_user)
):
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Մուտքը արգելված է։")

    return get_videos_by_warehouse(warehouse_id)

