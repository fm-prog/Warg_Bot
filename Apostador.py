import datetime
import re

#funcao = "/programar Arábia 11:06:00"
#funcao = funcao.replace("/programar ", "")
#funcao = funcao.split(" ")
#print(funcao)

#strdate="11:06:00"
#datetimeobj = datetime.datetime.strptime(strdate, "%H:%M:%S")
#time_now = datetime.datetime.now()
#time_now = time_now.strftime("%X")
#print(time_now)


def is_programar(string):
    reg_exp = r"/programar \w+ [0-2][0-9]:[0-5][0-9]:[0-5][0-9]"
    result = re.match(reg_exp, string)
    time_now = datetime.datetime.now()
    time_now = time_now.strftime("%X")
    time_now = time_now.split(":")
    hh = int(time_now[0])
    mm = int(time_now[1])

    if result:
        string = string.split(" ")
        tempo = string[-1]
        print(tempo)
        hora_limit = int(tempo[0] + tempo[1])
        time_limit = int(tempo[3] + tempo[4])
        print(hora_limit)
        print(time_limit)
        if hora_limit > 23 or (hora_limit <= hh and time_limit <= mm):
            return False

    return result

teste = "/programar Flamengo 19:44:59"

if is_programar(teste):
    print("Done!")


print(hash("programadores"))
