from typing import Dict, Any, List, Tuple
from datetime import date

class DeterministicEligibilityEngine:
    """
    Evaluates patient structured EHR features against protocol inclusion/exclusion criteria.
    Never permits LLMs to guess lab thresholds or biomarker matches.
    """

    def evaluate_criterion(
        self,
        criterion: Dict[str, Any],
        patient_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        c_type = criterion.get("criterion_type", "INCLUSION")
        category = criterion.get("category", "")
        desc = criterion.get("description", "")
        min_val = criterion.get("min_numeric_value")
        max_val = criterion.get("max_numeric_value")
        req_bio = criterion.get("required_biomarker")

        status = "PASS"
        reason = ""
        observed = ""

        # 1. AGE
        if category == "AGE":
            age = patient_data.get("age", 0)
            observed = f"Age: {age} years"
            if min_val is not None and age < min_val:
                status = "FAIL" if c_type == "INCLUSION" else "PASS"
                reason = f"Patient age ({age}) is below minimum requirement ({min_val})."
            elif max_val is not None and age > max_val:
                status = "FAIL" if c_type == "INCLUSION" else "PASS"
                reason = f"Patient age ({age}) exceeds maximum allowed ({max_val})."
            else:
                status = "PASS" if c_type == "INCLUSION" else "FAIL"
                reason = f"Patient age ({age}) satisfies criterion."

        # 2. ECOG PERFORMANCE STATUS
        elif category == "ECOG":
            ecog = patient_data.get("ecog_performance", 0)
            observed = f"ECOG PS: {ecog}"
            if max_val is not None and ecog > max_val:
                status = "FAIL" if c_type == "INCLUSION" else "PASS"
                reason = f"ECOG score ({ecog}) exceeds protocol limit (<= {int(max_val)})."
            else:
                status = "PASS" if c_type == "INCLUSION" else "FAIL"
                reason = f"ECOG score ({ecog}) within acceptable performance range."

        # 3. GENOMIC BIOMARKER
        elif category == "BIOMARKER":
            biomarkers = patient_data.get("biomarkers", [])
            observed = f"Biomarkers: {', '.join([f'{b.get('gene')} {b.get('mutation_variant')}' for b in biomarkers]) or 'None reported'}"
            matched = False
            if req_bio:
                req_upper = req_bio.upper().replace("_", " ")
                for b in biomarkers:
                    b_str = f"{b.get('gene', '')} {b.get('mutation_variant', '')}".upper()
                    if req_upper in b_str or (b.get("gene", "").upper() in req_upper and b.get("status", "").upper() == "POSITIVE"):
                        matched = True
                        break
            
            if c_type == "INCLUSION":
                if matched:
                    status = "PASS"
                    reason = f"Patient positive for required biomarker '{req_bio}'."
                else:
                    status = "FAIL"
                    reason = f"Required biomarker '{req_bio}' not confirmed in genomic profile."
            else: # EXCLUSION
                if matched:
                    status = "FAIL"
                    reason = f"Patient carries excluded biomarker alteration '{req_bio}'."
                else:
                    status = "PASS"
                    reason = f"Patient does not harbor excluded alteration '{req_bio}'."

        # 4. LABORATORY VALUES
        elif category == "LAB":
            labs = patient_data.get("labs", {})
            test_key = req_bio or ""
            lab_entry = labs.get(test_key.lower()) or {}
            val = lab_entry.get("value")
            unit = lab_entry.get("unit", "")
            
            if val is None:
                status = "UNKNOWN"
                reason = f"Lab test '{test_key}' not found in recent panels. Screening lab draw required."
                observed = "Lab result pending"
            else:
                observed = f"{test_key}: {val} {unit}"
                if min_val is not None and val < min_val:
                    # e.g. Inclusion requires >= 1.5. If val < 1.5, Inclusion fails.
                    status = "FAIL" if c_type == "INCLUSION" else "PASS"
                    reason = f"Lab value ({val} {unit}) below protocol threshold ({min_val})."
                elif max_val is not None and val > max_val:
                    # e.g. Exclusion prohibits > 1.5. If val > 1.5, Exclusion triggers, so patient FAILS.
                    status = "FAIL" if c_type == "EXCLUSION" else "FAIL"
                    reason = f"Lab value ({val} {unit}) exceeds threshold ({max_val})."
                else:
                    # Within safe range: Inclusion passes, Exclusion does not trigger (passes)
                    status = "PASS"
                    reason = f"Lab value ({val} {unit}) meets protocol safety criteria."

        # 5. PRIOR THERAPY / WASHOUT
        elif category == "PRIOR_THERAPY":
            prior = patient_data.get("prior_therapies", "")
            observed = f"Prior Lines: {prior or 'None'}"
            if req_bio and req_bio.lower() in prior.lower():
                status = "FAIL" if c_type == "EXCLUSION" else "PASS"
                reason = f"Patient received prior treatment '{req_bio}'."
            else:
                status = "PASS" if c_type == "EXCLUSION" else "FAIL"
                reason = f"No prohibitive prior therapy conflict identified."

        else:
            status = "PASS"
            reason = "General criteria met."
            observed = "Documented in EHR"

        return {
            "criterion_id": criterion.get("id"),
            "criterion_type": c_type,
            "category": category,
            "description": desc,
            "status": status,
            "observed_evidence": observed,
            "evaluation_reason": reason,
        }

    def evaluate_patient_for_trial(
        self,
        trial_criteria: List[Dict[str, Any]],
        patient_data: Dict[str, Any]
    ) -> Tuple[str, float, List[Dict[str, Any]]]:
        breakdown = []
        has_fail = False
        has_unknown = False

        pass_count = 0
        total_eval = len(trial_criteria) or 1

        for crit in trial_criteria:
            res = self.evaluate_criterion(crit, patient_data)
            breakdown.append(res)
            if res["status"] == "FAIL":
                has_fail = True
            elif res["status"] == "UNKNOWN":
                has_unknown = True
            elif res["status"] == "PASS":
                pass_count += 1

        if has_fail:
            overall = "INELIGIBLE"
            confidence = round(pass_count / total_eval, 2)
        elif has_unknown:
            overall = "UNCERTAIN"
            confidence = round(pass_count / total_eval, 2)
        else:
            overall = "ELIGIBLE"
            confidence = 0.98

        return overall, confidence, breakdown

eligibility_engine = DeterministicEligibilityEngine()
