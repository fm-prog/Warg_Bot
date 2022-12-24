# SuperFastPython.com
# example of using join and task_done with an asyncio queue
from random import random
import asyncio


# coroutine to generate work
async def producer(queue):
    print('Producer: Running')
    # generate work
    for i in range(10):
        # generate a value
        value = random()
        # block to simulate work
        #await asyncio.sleep(value)
        # add to the queue
        await queue.put(i)
    print('Producer: Done')


# coroutine to consume work
async def consumer(queue, name):
    print('Consumer: Running')
    # consume work
    while True:
        # get a unit of work
        item = await queue.get()
        # report
        print(f'>{name} got {item}')
        # block while processing
        #if item:
        await asyncio.sleep(item)
        # mark the task as done
        queue.task_done()


# entry point coroutine
async def main():
    # create the shared queue
    queue = asyncio.Queue()
    # start the consumer
    #_ = asyncio.create_task(consumer(queue, "B"))
    _ = asyncio.create_task(consumer(queue, "A"))
    #await asyncio.gather(consumer(queue, "A"))
    # start the producer and wait for it to finish
    await asyncio.create_task(producer(queue))
    # wait for all items to be processed
    await queue.join()


# start the asyncio program
asyncio.run(main())
















while not soloq_jogos.empty():

                try:
                    print(f"Ainda na soloq:{soloq_jogos.qsize()}")
                    jogo = await soloq_jogos.get()
                    print(f"Observador {rotina + 1} no jogo de número {jogo}!")
                    Observers.insert(rotina, f"Observador {rotina + 1} no jogo de número {jogo}!")
                    await match.nth(jogo).hover(timeout=0, force=True)
                    await match.nth(jogo).click()
                    if "(Esports)" not in await match.nth(jogo).inner_text():
                        if "(Simulação)" not in await match.nth(jogo).inner_text():
                            await pagina.wait_for_selector(".scoreboard__top")
                            score = await pagina.locator(".scoreboard__top").inner_text()
                            score_splt = score.split("\n")
                            casa = score_splt[0]
                            while casa not in await match.nth(jogo).inner_text():
                                score = await pagina.locator(".scoreboard__top").inner_text()
                                score_splt = score.split("\n")
                                casa = score_splt[0]

                            fora = score_splt[-1]
                            tempo = score_splt[-5]

                            if await is_placar(score_splt[-2]) and score_splt[-3] == "-":
                                print("Confirmei e é jogo!")
                            else:
                                break

                            if tempo == "0:00":
                                print("O jogo ainda não começou!")
                                continue

                            score_splt, stats_p, fatos_drop = await initial_monit(pagina)

                            try:

                                await pagina.wait_for_selector(".control-events-title")
                                await pagina.locator(".control-events-title").click()
                                await pagina.wait_for_selector(".dropdown-item")
                                drop = pagina.locator(".dropdown-item")

                                for d in range(await drop.count()):
                                    if await drop.nth(d).inner_text() == f"{casa} - {fora}":
                                        await pagina.locator(".control-events-title").click()
                                        stats_now = await normal_monit(pagina, score_splt, stats_p)
                                        break
                                else:
                                    await pagina.locator(".control-events-title").click()
                                    stats_now = await alt_monit(score_splt, stats_p, fatos_drop)

                            except Exception as error:
                                print(f"Deu merda, aqui o que foi: {error.__class__}")
                                print(error)
                                print(format_tb(error.__traceback__))
                                continue
                            else:
                                print(f"Observador {rotina + 1} no jogo de número {jogo}, terminou sua tarefa!")
                                soloq_jogos.task_done()
                                await trigger(stats_now)

                            if not ativo:
                                break


                except IndexError as error:
                    print(f"Deu out of range, vou continuar e tirar o item da lista: {error.__class__}")
                    print(error)
                    print(format_tb(error.__traceback__))
                    info = f'''
Deu merda, aqui no while da li_row_jogos, erro de range de lista: {error.__class__}\n
{error}\n
{format_tb(error.__traceback__)}\n
'''
                    print(f"Observador {rotina + 1} no jogo de número {jogo}, pulou a tarefa devido a um erro!")
                    logging.error(info)

                except Exception as error:
                    print(f"Deu merda, aqui o que foi: {error.__class__}")
                    print(error)
                    print(format_tb(error.__traceback__))
                    info = f'''
Deu merda, aqui no while da soloq, o que foi: {error.__class__}\n
{error}\n
{format_tb(error.__traceback__)}\n
'''
                    logging.error(info)
            else:
                print(f"Ainda na soloq:{soloq_jogos.qsize()}")

