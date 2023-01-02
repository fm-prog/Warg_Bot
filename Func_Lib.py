import datetime
import re
from difflib import SequenceMatcher
import logging


async def is_percent(string):
    reg_exp = r"[0-100] %"
    return re.match(reg_exp, string)


async def is_agendar(string):
    if string.isdigit():
        reg_exp = r"[1-999]"
    else:
        return False
    return re.match(reg_exp, string)


async def is_time(string):
    reg_exp = r"\w"
    return re.match(reg_exp, string)


async def is_programar(string):
    reg_exp = r"^[0-2][0-9]:[0-5][0-9]:[0-5][0-9]$"
    result = re.match(reg_exp, string)
    time_now = datetime.datetime.now()
    time_now = time_now.strftime("%X")
    time_now = time_now.split(":")
    hh = int(time_now[0])
    mm = int(time_now[1])

    if result:
        string = string.split(" ")
        tempo = string[-1]
        hora_limit = int(tempo[0] + tempo[1])
        time_limit = int(tempo[3] + tempo[4])
        if hora_limit > 23 or (hora_limit <= hh and time_limit <= mm):
            return False

    return result


async def is_drop(string):
    reg_exp = r"^[1-5]$"
    return re.match(reg_exp, string)


async def is_horario(string):
    reg_exp = r"\d+:\d+"
    return re.match(reg_exp, string)


async def is_prolongamento(string):
    reg_exp = r"\+\d+"
    return re.match(reg_exp, string)


async def is_tempo(string):
    reg_exp = r"\d+'"
    return re.match(reg_exp, string)


async def longestsubstring(str1, str2):
    seqmatch = SequenceMatcher(None, str1, str2)

    match = seqmatch.find_longest_match(0, len(str1), 0, len(str2))
    comp = SequenceMatcher(None, str1[match.a: match.a + match.size], str1)
    ratio = comp.ratio()

    if ratio > 0.80:
        print(f"Achei coincidencias: {str1[match.a: match.a + match.size]}")
        logging.info(f"Achei coincidencias: {str1[match.a: match.a + match.size]}")
        logging.info(f"Coincidiu acima de 80%: {ratio:.2%}")
        return True
    else:
        print(f"Achei coincidencias abaixo de 80%: {str1[match.a: match.a + match.size]}")
        logging.info(f"Achei coincidencias abaixo de 80%: {str1[match.a: match.a + match.size]}")
        logging.info(f"Coincidiu abaixo de 80%: {ratio:.2%}")
        return False


async def match(lance, alertas):
    for al in alertas:
        if al in lance:
            return True
    return False


async def is_placar(string):
    reg_exp = r"^\d+[-]\d+\s"
    return re.match(reg_exp, string) is not None


async def is_comand(string):
    reg_exp = r"^/"
    return re.match(reg_exp, string) is not None


async def is_valor(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
