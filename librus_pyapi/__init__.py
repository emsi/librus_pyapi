from urllib.parse import urljoin

import requests

from .schemas import (
    Message,
    MessageCollection,
    UnreadMessagesCount,
    AttachmentDownloadData,
)

CLIENT_ID = 46
SYNERGIA_DOMAIN = "synergia.librus.pl"
WIADOMOSCI_DOMAIN = "wiadomosci.librus.pl"
SYNERGIA_OAUTH_TOKEN_COOKIE = "oauth_token"
API_OAUTH_AUTHORIZATION_URL = (
    f"https://api.librus.pl/OAuth/Authorization?client_id={CLIENT_ID}"
)
API_OAUTH_AUTHORIZATION_WITH_SCOPE_URL = (
    f"{API_OAUTH_AUTHORIZATION_URL}&response_type=code&scope=mydata"
)
SYNERGIA_PORTAL_LOGIN_URL = "https://synergia.librus.pl/loguj/portalRodzina"
SYNERGIA_MESSAGES_BOOTSTRAP_URL = "https://synergia.librus.pl/wiadomosci3"
MAX_OAUTH_REDIRECTS = 10


class LibrusAPI:
    """
    Librus API client.
    """

    def __init__(self, login: str, password: str):
        """
        Initialize API client and authenticate the session.

        :param login: Librus login.
        :param password: Librus password.
        :return: None.
        """
        self.login = login
        self.password = password
        session = self.session = requests.Session()
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9,pl;q=0.8",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Origin": "https://api.librus.pl",
            "Pragma": "no-cache",
            "Referer": API_OAUTH_AUTHORIZATION_URL,
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }

        # Start OAuth via Synergia entrypoint to obtain oauth_state and keep the flow in Synergia context.
        response = session.get(SYNERGIA_PORTAL_LOGIN_URL, allow_redirects=False)
        response.raise_for_status()
        oauth_authorization_url = response.headers.get("Location")
        if not oauth_authorization_url:
            raise RuntimeError("Failed to initialize OAuth login flow for Synergia.")

        # Initialize authorization endpoint (sets API-side session cookies).
        response = session.get(
            oauth_authorization_url,
            allow_redirects=False,
        )
        response.raise_for_status()

        # Submit login credentials.
        data = {"action": "login", "login": login, "pass": password}
        response = session.post(
            API_OAUTH_AUTHORIZATION_URL,
            data=data,
            headers=self.headers,
        )
        response.raise_for_status()
        try:
            login_response = response.json()
        except ValueError as exc:
            raise RuntimeError("Unexpected login response format.") from exc

        go_to = login_response.get("goTo")
        if not go_to:
            raise RuntimeError("OAuth login response does not contain redirect target.")

        # Complete OAuth chain manually to preserve intermediate cookies (oauth_token).
        current_url = urljoin(API_OAUTH_AUTHORIZATION_WITH_SCOPE_URL, go_to)
        for _ in range(MAX_OAUTH_REDIRECTS):
            response = session.get(current_url, allow_redirects=False)
            response.raise_for_status()
            location = response.headers.get("Location")
            if not location:
                break
            current_url = urljoin(response.url, location)
        else:
            raise RuntimeError("OAuth login redirect limit exceeded.")

        if not any(
            cookie.name == SYNERGIA_OAUTH_TOKEN_COOKIE
            and cookie.domain.endswith(SYNERGIA_DOMAIN)
            for cookie in session.cookies
        ):
            raise RuntimeError("Synergia OAuth token was not created during login.")

        # Bootstrap MultiDomainLogon for wiadomości domain.
        response = session.get(SYNERGIA_MESSAGES_BOOTSTRAP_URL)
        response.raise_for_status()
        if "Brak dostępu" in response.text:
            raise RuntimeError("Access to Librus wiadomości was denied after login.")

        if not any(
            cookie.domain.endswith(WIADOMOSCI_DOMAIN) for cookie in session.cookies
        ):
            raise RuntimeError(
                "Wiadomości session bootstrap failed (missing domain cookie)."
            )

    def messages(
        self, page: int = 1, limit: int = 10, mailbox="inbox"
    ) -> MessageCollection:
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
        response = self.session.get(
            f"https://wiadomosci.librus.pl/api/{mailbox}/messages/senders"
        )
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

    def attachment(self, attachment_id: str, message_id: str):
        """
        Get attachment object by id.
        """
        response = self.session.get(
            f"https://wiadomosci.librus.pl/api/attachments/{attachment_id}/messages/{message_id}"
        )
        response.raise_for_status()
        return AttachmentDownloadData(**response.json()["data"])

    def grades(self):
        """
        Get grades.
        """
        response = self.session.get("https://synergia.librus.pl/gateway/api/2.0/Grades")
        response.raise_for_status()
        return response.json()
