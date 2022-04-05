import asyncio
import queue
import random
import threading
import time


class FakeFilter(object):

    def __init__(self, name: str, repo: queue.Queue):
        self.name = name
        self.repo = repo

    def get_new(self) -> str:
        try:
            return self.repo.get_nowait()
        except queue.Empty:
            return ''


def handle_event(name, event):
    print('handle', name, event)


async def log_loop(event_filter, poll_interval):
    while True:
        event = event_filter.get_new()
        if event:
            handle_event(event_filter.name, event)
        await asyncio.sleep(poll_interval)


def async_task():
    repo, interval = queue.Queue[str](), 2

    def add_event(repository: queue.Queue):
        while True:
            time.sleep(interval)
            repository.put(str(random.randint(100, 999)))
    threading.Thread(target=add_event, args=[repo], daemon=True).start()

    block_filter = FakeFilter('block', repo)
    tx_filter = FakeFilter('tx', repo)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(block_filter, interval),
                log_loop(tx_filter, interval)
            ))
    finally:
        loop.close()


if __name__ == '__main__':
    async_task()
