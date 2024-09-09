import requests

from .schemas import Message, MessageCollection, UnreadMessagesCount


class LibrusAPI:
    """
    Librus API client.
    """

    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password
        session = self.session = requests.Session()
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9,pl;q=0.8",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Length": "21",
            # "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "api.librus.pl",
            "Origin": "https://api.librus.pl",
            "Pragma": "no-cache",
            "Referer": "https://api.librus.pl/OAuth/Authorization?client_id=46",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }

        # Initial request
        response = session.get(
            "https://api.librus.pl/OAuth/Authorization?client_id=46&response_type=code&scope=mydata",
            allow_redirects=False,
        )
        response.raise_for_status()

        # Submitting login credentials
        data = {"action": "login", "login": login, "pass": password}
        response = session.post(
            "https://api.librus.pl/OAuth/Authorization?client_id=46",
            data=data,
            headers=self.headers,
        )
        response.raise_for_status()
        print(response.json())

        # Handle 2FA if needed
        response = session.get(
            f"https://api.librus.pl{response.json()['goTo']}",
            # allow_redirects=False,
        )
        response.raise_for_status()

        # add wiadomości API
        response = session.get("https://synergia.librus.pl/wiadomosci3")
        response.raise_for_status()

    def messages(self, page: int = 1, limit: int = 10, mailbox="inbox") -> MessageCollection:
        """
        Get messages from mailbox.
        """
        response = self.session.get(
            f"https://wiadomosci.librus.pl/api/{mailbox}/messages?page={page}&limit={limit}"
        )
        response.raise_for_status()
        return MessageCollection(**response.json())

    def unread_messages(
        self, mailbox="inbox", page: int = 1, limit: int = 10
    ) -> MessageCollection:
        """
        Get unread messages from mailbox.
        """
        response = self.session.get(
            f"https://wiadomosci.librus.pl/api/{mailbox}/messages?unreadOnly=1&page={page}&limit={limit}"
        )
        response.raise_for_status()
        return MessageCollection(**response.json())

    def unread_messages_count(self, mailbox="inbox") -> UnreadMessagesCount:
        """
        Get unread messages counts.
        """
        response = self.session.get(
            f"https://wiadomosci.librus.pl/api/{mailbox}/unreadMessagesCount"
        )
        response.raise_for_status()
        return UnreadMessagesCount(**response.json()["data"])

    def senders(self, mailbox="inbox"):
        """
        Get senders.
        """
        response = self.session.get(f"https://wiadomosci.librus.pl/api/{mailbox}/messages/senders")
        response.raise_for_status()
        return response.json()

    def message(self, message_id, mailbox="inbox") -> Message:
        """
        Get message by id.
        """
        response = self.session.get(
            f"https://wiadomosci.librus.pl/api/{mailbox}/messages/{message_id}"
        )
        response.raise_for_status()
        return Message(**response.json()["data"])

    def signatures(self):
        """
        Get signatures.
        """
        response = self.session.get("https://wiadomosci.librus.pl/api/signatures")
        response.raise_for_status()
        return response.json()

    def tags(self):
        """
        Get tags.
        """
        response = self.session.get("https://wiadomosci.librus.pl/api/tags")
        response.raise_for_status()
        return response.json()

    def types(self):
        """
        Get types.
        """
        response = self.session.get(
            "https://wiadomosci.librus.pl/api/receivers/types?includeClass=true"
        )
        response.raise_for_status()
        return response.json()
