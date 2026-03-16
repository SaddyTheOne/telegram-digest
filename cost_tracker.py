import json
import calendar
from datetime import datetime
from pathlib import Path

import config

COST_FILE = Path(__file__).parent / "cost_history.json"

INPUT_PRICE_PER_M = 3.0
OUTPUT_PRICE_PER_M = 15.0

DEFAULT_DATA = {
    "monthly_budget": config.MONTHLY_BUDGET,
    "current_month": datetime.now().strftime("%Y-%m"),
    "month_spent": 0.0,
    "total_spent": 0.0,
}


def _load() -> dict:
    if COST_FILE.exists():
        return json.loads(COST_FILE.read_text())
    return dict(DEFAULT_DATA)


def _save(data: dict) -> None:
    COST_FILE.write_text(json.dumps(data, indent=2) + "\n")


def calculate_cost(usage: dict) -> float:
    input_cost = usage["input_tokens"] / 1_000_000 * INPUT_PRICE_PER_M
    output_cost = usage["output_tokens"] / 1_000_000 * OUTPUT_PRICE_PER_M
    return round(input_cost + output_cost, 4)


def record_cost(cost: float) -> dict:
    data = _load()
    current = datetime.now().strftime("%Y-%m")

    if data["current_month"] != current:
        data["current_month"] = current
        data["month_spent"] = 0.0

    data["month_spent"] = round(data["month_spent"] + cost, 4)
    data["total_spent"] = round(data["total_spent"] + cost, 4)
    data["monthly_budget"] = config.MONTHLY_BUDGET

    _save(data)
    return data


def format_cost_line(cost: float, data: dict) -> str:
    month_num = int(data["current_month"].split("-")[1])
    month_name = calendar.month_name[month_num]
    return (
        f"💰 This digest: ${cost:.4f} | "
        f"{month_name}: ${data['month_spent']:.2f} / ${data['monthly_budget']:.2f}"
    )
