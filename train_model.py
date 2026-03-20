"""
Train a RandomForest classifier on the existing placements data.
Run this once: python ml/train_model.py
It saves model.joblib which FastAPI loads at startup.
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../placements_featured.csv"))

# Build target: derive primary recommendation from features
def get_label(row):
    if row["Placement_Readiness"] == "High" and row["Academic_Risk"] == "Low":
        return "Immediate Job"
    elif row["Academic_Risk"] == "High":
        return "Wait & Improve"
    elif row["Placement_Readiness"] == "Low":
        return "Skill Improvement"
    elif row["Higher Studies"] == "Yes":
        return "Higher Studies"
    elif row["Placement_Readiness"] == "Medium":
        return "Skill Improvement"
    else:
        return "Immediate Job"

df["Label"] = df.apply(get_label, axis=1)

# Encode categorical features
le_exp = LabelEncoder()
le_risk = LabelEncoder()
le_ready = LabelEncoder()
le_label = LabelEncoder()

df["exp_enc"]   = le_exp.fit_transform(df["Experience_Level"])
df["risk_enc"]  = le_risk.fit_transform(df["Academic_Risk"])
df["ready_enc"] = le_ready.fit_transform(df["Placement_Readiness"])
df["label_enc"] = le_label.fit_transform(df["Label"])

features = ["Skill_Count", "exp_enc", "risk_enc", "ready_enc", "Backlogs", "Internships", "Projects Completed"]
X = df[features]
y = df["label_enc"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

acc = accuracy_score(y_test, clf.predict(X_test))
print(f"Model accuracy: {acc:.2%}")

out_path = os.path.join(os.path.dirname(__file__), "model.joblib")
joblib.dump({
    "model": clf,
    "le_exp": le_exp,
    "le_risk": le_risk,
    "le_ready": le_ready,
    "le_label": le_label,
    "features": features
}, out_path)

print(f"Model saved to {out_path}")
