from base64 import b64decode
from typing import List, Optional

from pydantic import BaseModel, validator


class MessageSnippet(BaseModel):
    """
    Message snippets as shown on the inbox view.
    """

    messageId: str
    senderFirstName: str
    senderLastName: str
    senderName: str
    topic: str
    content: str
    sendDate: str | None
    readDate: str | None
    tags: List
    category: Optional[None]
    otherNodeUuid: Optional[None]
    otherNodeAccountId: Optional[None]
    isAnyFileAttached: bool

    @validator("content", pre=True, always=True)
    def decode_base64(cls, v):
        try:
            return b64decode(v).decode("utf-8", errors="replace")
        except Exception as e:
            raise ValueError(f"Error decoding base64 content: {str(e)}")


class MessageCollection(BaseModel):
    """
    Collection of message snippets.
    """

    data: List[MessageSnippet]
    total: int


class Receiver(BaseModel):
    """
    Receiver of the message.
    """

    receiverId: str
    firstName: str | None
    lastName: str | None
    className: str | None
    pupilFirstName: str | None
    pupilLastName: str | None
    group: str | None
    active: str | int | None
    otherNodeUuid: Optional[None]
    otherNodeAccountId: Optional[None]
    isCc: str | None
    isBcc: str | None
    name: str | None
    groupId: str | None


class Message(BaseModel):
    """
    Full message object.
    """

    messageId: str
    receiver: str
    senderId: str
    senderFirstName: str
    senderLastName: str
    senderGroup: str
    myMessage: str
    topic: str
    Message: str
    sendDate: str
    readDate: str | None
    spam: str
    state: str
    otherNodeUuid: Optional[None]
    otherNodeAccountId: Optional[None]
    otherNodeMessageId: Optional[None]
    userFirstName: str | None
    userLastName: str
    userClass: str
    applicationNumber: Optional[None]
    originalMessage: str
    originalTopic: str
    noReply: int
    archive: int
    senderSchoolName: Optional[None]
    senderGroupId: str
    senderName: str
    attachementInfo: str
    attachments: List
    enableMessageWithdrawn: int
    isMessageWithdrawn: int
    receiversCount: int
    readedCount: int
    receivers: List[Receiver]
    tags: List

    @validator("Message", pre=True, always=True)
    def decode_base64(cls, v):
        try:
            return b64decode(v).decode("utf-8", errors="replace")
        except Exception as e:
            raise ValueError(f"Error decoding base64 message: {str(e)}")


class UnreadMessagesCount(BaseModel):
    """
    Unread messages counts.
    """

    inbox: int
    notes: int
    alerts: int
    substitutions: int
    absences: int
    justifications: int
    trash: int
    archiveInbox: int
    archiveNotes: int
    archiveAlerts: int
    archiveSubstitutions: int
    archiveAbsences: int
    archiveJustifications: int
    archiveTrash: int
