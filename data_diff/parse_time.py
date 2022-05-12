import re
from datetime import datetime, timedelta
from difflib import SequenceMatcher

TIME_UNITS = dict(
    seconds="seconds",
    minutes="minutes",
    hours="hours",
    days="days",
    weeks="weeks",
    months="months",
    years="years",
    # Shortcuts
    s="seconds",
    min="minutes",
    h="hours",
    d="days",
    w="weeks",
    mon="months",
    y="years",
)

EXTRAPOLATED = {"months": (30, "days"), "years": (365, "days")}
assert set(EXTRAPOLATED) <= set(TIME_UNITS)

TIME_RE = re.compile(r"(\d+)([a-z]+)")


def string_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def parse_time_atom(count, unit):
    count = int(count)
    try:
        unit = TIME_UNITS[unit]
    except KeyError:
        most_similar = max(TIME_UNITS, key=lambda k: string_similarity(k, unit))
        raise ValueError(f"'{unit}' is not a recognized time unit. Did you mean '{most_similar}'?")

    if unit in EXTRAPOLATED:
        mul, unit = EXTRAPOLATED[unit]
        count *= mul
    return count, unit


def parse_time_delta(t: str):
    time_dict = {}
    while t:
        m = TIME_RE.match(t)
        if not m:
            raise ValueError(f"Cannot parse '{t}': Not a recognized time delta")
        count, unit = parse_time_atom(*m.groups())
        if unit in time_dict:
            raise ValueError(f"Time unit {unit} specified more than once")
        time_dict[unit] = count
        t = t[m.end() :]

    if not time_dict:
        raise ValueError("No time difference specified")
    return datetime.now() - timedelta(**time_dict)