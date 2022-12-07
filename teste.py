import string
import time
from itertools import product

a = list(string.ascii_lowercase)
b = list(string.digits)
c = a + b

arranjo_com_rep = list(product(c, repeat=4))

senha = input("Informe a senha!")

print(len(senha))

t_inicial = time.time()


def produto(*args, repeat):
    # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
    # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
    pools = [tuple(pool) for pool in args] * repeat
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)


arranjo_com_rep = list(produto(c, repeat=len(senha)))


for i in arranjo_com_rep:

    str = ''.join(i)
    if str == senha:
        t_final = time.time()
        print(f"A senha é: {str}, demorei {t_final - t_inicial}")






