import asyncio
import itertools
import sys


@asyncio.coroutine
def spin(msg):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle("|/-\\"):
        status = char + " " + msg
        write(status)
        flush()
        write('\b' * len(status))
        try:
            yield from asyncio.sleep(.1)
        except asyncio.CancelledError:
            break
    write("over")


@asyncio.coroutine
def slow_function():
    yield from asyncio.sleep(3)
    return 42


@asyncio.coroutine
def supervisor():
    spinner = asyncio.async(spin('thinking!'))
    res = yield from slow_function()
    spinner.cancel()
    return res


def main():
    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(supervisor())
    loop.close()
    print(res)


main()
