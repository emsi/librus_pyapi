# Unofficial Librus Python API

This is an unofficial Python API for Librus Synergia. It allows you to interact with the Librus Synergia platform email system programmatically.
It's the only api client that I know of that interacts with the new email system directly via API and is not using HTMl scraping. 

## Compatibility update (2026-03-28)

Version `0.2.0` is compatible with Librus authentication changes introduced on 2026-03-28, including the Synergia OAuth bootstrap and MultiDomainLogon flow required for `wiadomosci.librus.pl` API access.

## Installation

This project is now managed with [uv](https://github.com/astral-sh/uv) for modern Python package management.

### Using uv (recommended)

```bash
# Install the package
uv pip install librus_pyapi

# Or install from source
uv pip install -e .

# For development
uv sync --extra dev
```

### Traditional pip

```bash
pip install librus_pyapi
```

W ogóle nie wiem czemu piszę to po angielsku. Chyba z przyzwyczajenia.

## Usage

```python

from librus_pyapi import LibrusAPI

api = LibrusAPI("login", "pasłord")

# listuje wiadomości z inboxa:
# def massages(self, page: int = 1, limit: int = 10, mailbox="inbox") -> MessageCollection:
api.messages()

# listuje nieprzeczytane:
# def unread_messages_count(self, mailbox="inbox") -> UnreadMessagesCount:
api.unread_messages_count()

# zwraca całą treść wiadomości:
# def message(self, message_id, mailbox="inbox") -> Message:
api.message(message_id).Message
```

There's more api, see the source code.
If you want to implement more, feel free to send PR.

# Serdecznie współczuję wszystkim, którzy muszą korzystać z Librusa.
