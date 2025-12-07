from datetime import datetime, time
from typing import Tuple


def parse_time_range(start: str, end: str) -> Tuple[time, time]:
    start_dt = datetime.strptime(start, "%H:%M").time()
    end_dt = datetime.strptime(end, "%H:%M").time()
    return start_dt, end_dt


def ranges_overlap(a_start: str, a_end: str, b_start: str, b_end: str) -> bool:
    a_s, a_e = parse_time_range(a_start, a_end)
    b_s, b_e = parse_time_range(b_start, b_end)
    return max(a_s, b_s) < min(a_e, b_e)


