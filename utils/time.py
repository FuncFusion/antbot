from re import compile, findall

from utils.validator import validate

measure_aliases = {
    "second": ["секунда", "секунд", "сек", "с", "seconds", "sec", "s"],
    "minute": ["минута", "минут", "мин", "м", "minutes", "min", "m"],
    "hour": ["час", "часа", "часов", "ч", "hours", "h"],
    "day": ["день", "дня", "дней", "сутки", "д", "d"],
    "week": ["неделя", "недели", "нд", "н", "w"],
    "month": ["месяц", "месяца", "месяцев", "мес", "ме", "mo"],
    "year": ["год", "лет", "г", "yr", "y"]
}
measure_multipliers = {
    "second": 1,
    "minute": 60,
    "hour": 3600,
    "day": 86400,
    "week": 604800,
    "month": 2592000,
    "year": 31536000
}

time_re = compile(r'([0-9]+)\s*([a-я]+)')

def get_secs(time):
    times = findall(time_re, time)
    secs = 0
    for num, measure in times:
        try:
            secs += int(num) * measure_multipliers[validate(measure, measure_aliases)]
        except:pass
    return secs
