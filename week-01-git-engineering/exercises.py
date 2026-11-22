"""Week 0: Python Fundamentals Bootcamp — Beginner Practice Tasks."""

import csv
import json
from typing import Dict, List, Tuple, Any


def evaluate_attendance_status(attended: int, total: int) -> str:
    """Return 'ELIGIBLE' (>=75%), 'WARNING' (65% to <75%), or 'SHORTAGE' (<65%).

    If total <= 0, return 'NO_SESSIONS'.
    """
    if total <= 0:
        return "NO_SESSIONS"

    percentage = (attended / total) * 100
    if percentage >= 75:
        return "ELIGIBLE"
    if percentage >= 65:
        return "WARNING"
    return "SHORTAGE"


def safe_parse_float(raw_value: Any, default: float = 0.0) -> float:
    """Convert raw_value to float safely using try/except. Return default on failure."""
    try:
        return float(raw_value)
    except (TypeError, ValueError, OverflowError):
        return default


def analyze_pod_scores(records: List[Tuple[str, str, float]]) -> Dict[str, Any]:
    """Analyze (usn, pod_name, score) tuples using simple lists and a dictionary.

    Returns a dictionary with keys:
      - 'unique_student_count': int (number of unique USNs via set)
      - 'high_scorers': List[str] (USNs with score >= 80)
      - 'pod_averages': Dict[str, float] (average score per pod rounded to 2 decimals)
    """
    students = set()
    high_scorers = []
    pod_scores = {}

    for usn, pod_name, score in records:
        students.add(usn)

        if score >= 80 and usn not in high_scorers:
            high_scorers.append(usn)

        if pod_name not in pod_scores:
            pod_scores[pod_name] = []
        pod_scores[pod_name].append(score)

    pod_averages = {}
    for pod_name in pod_scores:
        scores = pod_scores[pod_name]
        average = sum(scores) / len(scores)
        pod_averages[pod_name] = round(average, 2)

    return {
        "unique_student_count": len(students),
        "high_scorers": high_scorers,
        "pod_averages": pod_averages,
    }


def summarize_csv_to_json(csv_path: str, json_path: str) -> Dict[str, Any]:
    """Read cohort CSV using built-in csv module and export summary JSON.

    Summary dictionary must contain:
      - 'total_students': int
      - 'branches': List[str] (sorted unique branch codes)
      - 'average_score': float (rounded to 2 decimals)
    """
    rows = []
    with open(csv_path, "r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            rows.append(row)

    branches = []
    total_score = 0

    for row in rows:
        branch = row["branch"]
        if branch not in branches:
            branches.append(branch)
        total_score = total_score + float(row["score"])

    total_students = len(rows)
    if total_students > 0:
        average_score = round(total_score / total_students, 2)
    else:
        average_score = 0.0

    summary = {
        "total_students": total_students,
        "branches": sorted(branches),
        "average_score": average_score,
    }

    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(summary, json_file, indent=2)

    return summary


class StudentRecord:
   

    def __init__(self, usn: str, name: str):
        self.usn = usn.upper()
        self.name = name
        self.scores: List[float] = []

    def add_score(self, score: float) -> None:
        if score < 0 or score > 100:
            raise ValueError("score must be between 0 and 100")
        self.scores.append(score)

    def average(self) -> float:
        if len(self.scores) == 0:
            return 0.0

        total = sum(self.scores)
        count = len(self.scores)
        return round(total / count, 2)

    def is_passing(self, threshold: float = 50.0) -> bool:
        return self.average() >= threshold
