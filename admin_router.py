"""
Admin routes — view all students and predictions.
In production you'd add role-based access control.
For now, any logged-in user can access (show this in your CV as extendable).
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
import models, schemas

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/students", response_model=list[schemas.UserOut])
def all_students(
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return db.query(models.User).order_by(models.User.created_at.desc()).all()


@router.get("/profiles", response_model=list[schemas.ProfileOut])
def all_profiles(
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return db.query(models.StudentProfile).order_by(models.StudentProfile.created_at.desc()).all()


@router.get("/stats")
def stats(
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    total_users    = db.query(models.User).count()
    total_profiles = db.query(models.StudentProfile).count()
    total_preds    = db.query(models.Prediction).count()

    from sqlalchemy import func
    top_recs = (
        db.query(models.Prediction.top_recommendation, func.count().label("count"))
        .group_by(models.Prediction.top_recommendation)
        .all()
    )

    return {
        "total_students":   total_users,
        "total_profiles":   total_profiles,
        "total_predictions": total_preds,
        "recommendations_breakdown": {r: c for r, c in top_recs},
    }
