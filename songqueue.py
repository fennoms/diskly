"""This file holds a queue data structure that can be
used to make a queue of songs to play."""

type URL = str


class Queue:
    def __init__(self):
        # We can use a normal list because
        # we assume this bot will be used for small servers,
        # thus removing and adding songs should still be fast.
        self.queue = []

    async def add(self, song: URL, title: str):
        """Add a song to the queue.

        Args:
            song (URL): a URL to a song.
        """
        self.queue.append((song, title))

    async def pop(self, index: int):
        """Remove a song from the queue.

        Args:
            index (int): the index of the song to remove.
        """
        song, title = self.queue.pop(index)
        return song, title

    async def clear(self):
        """Clear the queue."""
        self.queue.clear()

    def __str__(self):
        if len(self.queue) == 0:
            return "🎵 Queue is empty!"

        titles = [f"{i + 1}. {title}" for i, (_, title) in enumerate(self.queue)]
        return "🎵 Queue " + "\n".join(titles)
