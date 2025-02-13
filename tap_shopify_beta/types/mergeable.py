from singer_sdk import typing as th

class MergeableType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("errorFields", th.ArrayType(th.StringType)),
            th.Property("isMergeable", th.BooleanType),
            th.Property("mergeInProgress", th.ObjectType(
                th.Property("customerMergeErrors", th.ArrayType(th.ObjectType(
                    th.Property("errorFields", th.ArrayType(th.StringType)),
                    th.Property("message", th.StringType),
                ))),
                th.Property("jobId", th.StringType),
                th.Property("resultingCustomerId", th.StringType),
                th.Property("status", th.StringType),
            )),
            th.Property("reason", th.StringType),
        )
