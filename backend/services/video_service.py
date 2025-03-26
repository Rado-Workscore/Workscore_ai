from backend.database import SessionLocal
from backend.models.video import Video
from backend.schemas.video import VideoCreate, VideoOut
from typing import List

def create_video(data: VideoCreate) -> VideoOut:
    db = SessionLocal()
    new_video = Video(
        filename=data.filename,
        warehouse_id=data.warehouse_id,
        camera_id=data.camera_id,
    )
    db.add(new_video)
    db.commit()
    db.refresh(new_video)
    db.close()
    return new_video

def get_videos_by_warehouse(warehouse_id: int) -> List[VideoOut]:
    db = SessionLocal()
    videos = db.query(Video).filter(Video.warehouse_id == warehouse_id).all()
    db.close()
    return videos
