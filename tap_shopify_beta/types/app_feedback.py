from singer_sdk import typing as th

from tap_shopify_beta.types.link import LinkType
from tap_shopify_beta.types.user_error import UserErrorType

class AppFeedbackType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("link", LinkType()),
            th.Property("messages", th.ArrayType(UserErrorType()))
        )
