import json
import os
import joblib
import numpy as np
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
import models, schemas
from dss_engine import compute_features, rule_based_scores, rank_options

router = APIRouter(prefix="/predict", tags=["Predictions"])

# Load ML model once at startup
_model_path = os.path.join(os.path.dirname(__file__), "../ml/model.joblib")
_bundle = joblib.load(_model_path)
_clf      = _bundle["model"]
_le_exp   = _bundle["le_exp"]
_le_risk  = _bundle["le_risk"]
_le_ready = _bundle["le_ready"]
_le_label = _bundle["le_label"]


def _ml_predict(features: dict, backlogs: int, internships: int, projects: int):
    exp_enc   = _le_exp.transform([features["experience_level"]])[0]
    risk_enc  = _le_risk.transform([features["academic_risk"]])[0]
    ready_enc = _le_ready.transform([features["placement_readiness"]])[0]

    X = np.array([[
        features["skill_count"],
        exp_enc,
        risk_enc,
        ready_enc,
        backlogs,
        internships,
        projects,
    ]])

    proba = _clf.predict_proba(X)[0]
    pred_idx = np.argmax(proba)
    label = _le_label.inverse_transform([pred_idx])[0]
    confidence = float(round(proba[pred_idx], 4))
    return label, confidence


@router.post("/", response_model=schemas.PredictionOut, status_code=201)
def submit_and_predict(
    payload: schemas.ProfileCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    # 1. Compute engineered features
    feats = compute_features(
        skills=payload.skills,
        backlogs=payload.backlogs,
        projects=payload.projects,
        internships=payload.internships,
    )

    # 2. Save profile to PostgreSQL
    profile = models.StudentProfile(
        user_id=current_user.id,
        skills=payload.skills,
        backlogs=payload.backlogs,
        projects=payload.projects,
        internships=payload.internships,
        higher_studies_interest=payload.higher_studies_interest,
        skill_count=feats["skill_count"],
        experience_level=feats["experience_level"],
        academic_risk=feats["academic_risk"],
        placement_readiness=feats["placement_readiness"],
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)

    # 3. ML prediction
    ml_rec, ml_conf = _ml_predict(
        feats, payload.backlogs, payload.internships, payload.projects
    )

    # 4. Rule-based scores
    scores = rule_based_scores(feats, higher_studies=payload.higher_studies_interest)
    ranked = rank_options(scores)

    # 5. Save prediction to PostgreSQL
    prediction = models.Prediction(
        user_id=current_user.id,
        profile_id=profile.id,
        ml_recommendation=ml_rec,
        ml_confidence=ml_conf,
        rule_scores=json.dumps([{"option": k, "score": v} for k, v in ranked]),
        top_recommendation=ml_rec,
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return schemas.PredictionOut(
        id=prediction.id,
        ml_recommendation=ml_rec,
        ml_confidence=ml_conf,
        top_recommendation=ml_rec,
        rule_scores=[schemas.RankedOption(option=k, score=v) for k, v in ranked],
        created_at=prediction.created_at,
    )


@router.get("/history", response_model=list[schemas.PredictionOut])
def my_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    preds = (
        db.query(models.Prediction)
        .filter(models.Prediction.user_id == current_user.id)
        .order_by(models.Prediction.created_at.desc())
        .all()
    )
    result = []
    for p in preds:
        rule_scores = [schemas.RankedOption(**x) for x in json.loads(p.rule_scores)]
        result.append(schemas.PredictionOut(
            id=p.id,
            ml_recommendation=p.ml_recommendation,
            ml_confidence=p.ml_confidence,
            top_recommendation=p.top_recommendation,
            rule_scores=rule_scores,
            created_at=p.created_at,
        ))
    return result
