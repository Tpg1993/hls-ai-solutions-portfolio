import numpy as np
from typing import Dict, Any, Tuple, List
from sklearn.ensemble import GradientBoostingClassifier

class SiteEnrollmentRiskEngine:
    def __init__(self):
        self.model = GradientBoostingClassifier(n_estimators=60, max_depth=3, random_state=42)
        self._fit_pretrained_model()

    def _fit_pretrained_model(self):
        # Synthetic operational training vectors:
        # [velocity, failure_rate, delay_days, dropout_rate, enrollment_ratio]
        X = np.array([
            # Low Risk: high velocity, low failure, fast activation, high enrollment
            [4.5, 0.15, 14, 0.03, 0.95],
            [3.8, 0.20, 21, 0.05, 0.88],
            [5.0, 0.12, 10, 0.02, 1.05],
            [4.0, 0.18, 18, 0.04, 0.85],
            # Medium Risk: moderate velocity, average failure
            [2.0, 0.35, 45, 0.08, 0.55],
            [2.2, 0.30, 40, 0.07, 0.60],
            [1.8, 0.38, 50, 0.09, 0.50],
            [2.5, 0.28, 35, 0.06, 0.65],
            # High Risk: low velocity, high screen failure, severe delay, low enrollment
            [0.5, 0.65, 110, 0.22, 0.15],
            [0.8, 0.55, 90, 0.18, 0.20],
            [0.2, 0.70, 130, 0.25, 0.10],
            [0.6, 0.60, 100, 0.20, 0.18],
        ])
        # 0: Low Risk, 1: Medium Risk, 2: High Risk
        y = np.array([0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2])
        self.model.fit(X, y)

    def predict_site_risk(
        self,
        screening_velocity: float,
        screen_failure_rate: float,
        activation_delay_days: int,
        dropout_rate: float,
        target_patients: int,
        actual_enrolled: int
    ) -> Tuple[str, float, List[str]]:
        ratio = round(actual_enrolled / max(1, target_patients), 3)
        features = np.array([[
            screening_velocity,
            screen_failure_rate,
            float(activation_delay_days),
            dropout_rate,
            ratio
        ]])

        probs = self.model.predict_proba(features)[0]
        # P(High Risk)
        high_risk_prob = float(probs[2]) if len(probs) > 2 else 0.5

        if high_risk_prob >= 0.55 or ratio < 0.25:
            tier = "High"
        elif high_risk_prob >= 0.25 or ratio < 0.65:
            tier = "Medium"
        else:
            tier = "Low"

        # Key drivers
        drivers = []
        if screen_failure_rate >= 0.40:
            drivers.append(f"Excessive Screen Failure Rate ({screen_failure_rate*100:.1f}%)")
        if activation_delay_days >= 60:
            drivers.append(f"Institutional Activation Delay ({activation_delay_days} days)")
        if screening_velocity < 1.2:
            drivers.append(f"Low Screening Velocity ({screening_velocity:.1f} patients/mo)")
        if ratio < 0.40:
            drivers.append(f"Enrollment Gap ({actual_enrolled}/{target_patients} target)")
        if not drivers:
            drivers.append(f"Normal Operations (Velocity: {screening_velocity:.1f}/mo, Failure: {screen_failure_rate*100:.1f}%)")

        return tier, round(high_risk_prob, 3), drivers

site_risk_engine = SiteEnrollmentRiskEngine()
