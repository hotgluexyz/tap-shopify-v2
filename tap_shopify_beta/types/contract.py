from singer_sdk import typing as th

from tap_shopify_beta.types.app import AppType
from tap_shopify_beta.types.count import CountType
from tap_shopify_beta.types.custom_attributes import CustomAttributesType
from tap_shopify_beta.types.customer import CustomerType
from tap_shopify_beta.types.customer_payment_method import CustomerPaymentMethodType
from tap_shopify_beta.types.money_v2 import MoneyV2Type

class ContractType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("app", AppType()),
            th.Property("appAdminUrl", th.StringType),
            th.Property("billingPolicy", th.ObjectType(
                th.Property("anchors", th.ArrayType(th.ObjectType(
                    th.Property("cutoffDay", th.IntegerType),
                    th.Property("day", th.IntegerType),
                    th.Property("month", th.IntegerType),
                    th.Property("type", th.StringType),
                ))),
                th.Property("interval", th.StringType),
                th.Property("intervalCount", th.IntegerType),
                th.Property("maxCycles", th.IntegerType),
                th.Property("minCycles", th.IntegerType),
            )),
            th.Property("createdAt", th.DateTimeType),
            th.Property("currencyCode", th.StringType),
            th.Property("customAttributes", CustomAttributesType()),
            th.Property("customer", CustomerType()),
            th.Property("customerPaymentMethod", CustomerPaymentMethodType()),
            th.Property("deliveryMethod", th.StringType),
            th.Property("deliveryPolicy", th.ObjectType(
                th.Property("anchors", th.ArrayType(th.ObjectType(
                    th.Property("cutoffDay", th.IntegerType),
                    th.Property("day", th.IntegerType),
                    th.Property("month", th.IntegerType),
                    th.Property("type", th.StringType),
                ))),
                th.Property("interval", th.StringType),
                th.Property("intervalCount", th.IntegerType),
            )),
            th.Property("deliveryPrice", MoneyV2Type()),
            th.Property("id", th.StringType),
            th.Property("lastPaymentStatus", th.StringType),
            # th.Property("linesCount", CountType()),
            th.Property("nextBillingDate", th.DateTimeType),
            th.Property("note", th.StringType),
            th.Property("revisionId", th.IntegerType),
            th.Property("status", th.StringType),
            th.Property("updatedAt", th.DateTimeType),
        )