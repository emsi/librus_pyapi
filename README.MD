# Unofficial Librus Python API

This is an unofficial Python API for Librus Synergia. It allows you to interact with the Librus Synergia platform programmatically.

## Installation

There is no installation instruction on purpose. If you want to use it you should know how to use python packages. 
I'm sorry. It acts as a filter. Code is very simple, just see for yourself.

W ogóle nie wiem czemu piszę to po angielsku. Chyba z przyzwyczajenia.

## Usage

```python

from librus_pyapi import LibrusAPI

api = LibrusAPI("login", "pasłord")

# listuje wiadomości z inboxa:
# def massages(self, page: int = 1, limit: int = 10, mailbox="inbox") -> MessageCollection:
api.massages()

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
