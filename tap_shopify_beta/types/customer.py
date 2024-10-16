from singer_sdk import typing as th

from tap_shopify_beta.types.image import ImageType
from tap_shopify_beta.types.money_v2 import MoneyV2Type
from tap_shopify_beta.types.mailing_address import MailingAddressType
from tap_shopify_beta.types.company_contact import CompanyContactType
from tap_shopify_beta.types.market import MarketType


class CustomerType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("addresses", th.ArrayType(MailingAddressType())),
            th.Property("amountSpent", MoneyV2Type()),
            th.Property("canDelete", th.BooleanType),
            th.Property("companyContactProfiles", th.ArrayType(CompanyContactType())),
            th.Property("createdAt", th.DateTimeType),
            # th.Property("dataSaleOptOut", th.BooleanType),
            th.Property("displayName", th.StringType),
            th.Property("email", th.StringType),
            th.Property("emailMarketingConsent", th.ObjectType(
                th.Property("consentUpdatedAt", th.DateTimeType),
                th.Property("marketingOptInLevel", th.DateTimeType),
                th.Property("marketingState", th.DateTimeType),
            )),
            th.Property("firstName", th.StringType),
            th.Property("id", th.StringType),
            th.Property("image", ImageType()),
            th.Property("lastName", th.StringType),
            th.Property("legacyResourceId", th.IntegerType),
            th.Property("lifetimeDuration", th.StringType),
            th.Property("locale", th.StringType),
            th.Property("market", MarketType()),
            th.Property("mergeable", th.ObjectType(
                th.Property("errorFields", th.ArrayType(th.StringType)),
                th.Property("isMergeable", th.BooleanType),
                th.Property("mergeInProgress", th.ObjectType(
                    th.Property("customerMergeErrors", th.ArrayType(th.ObjectType(
                        th.Property("errorFields", th.ArrayType(th.StringType)),
                        th.Property("message", th.StringType),
                    )),
                    th.Property("jobId", th.StringType),
                    th.Property("resultingCustomerId", th.StringType),
                    th.Property("status", th.StringType),
                ))),
                th.Property("reason", th.StringType),
            )),
            th.Property("multipassIdentifier", th.StringType),
            th.Property("note", th.StringType),
            th.Property("numberOfOrders", th.IntegerType),
            th.Property("phone", th.StringType),
            th.Property("productSubscriberStatus", th.StringType),
            th.Property("smsMarketingConsent", th.ObjectType(
                th.Property("consentCollectedFrom", th.StringType),
                th.Property("consentUpdatedAt", th.DateTimeType),
                th.Property("marketingOptInLevel", th.StringType),
                th.Property("marketingState", th.StringType),
            )),
            th.Property("state", th.StringType),
            th.Property("statistics", th.ObjectType(
                th.Property("predictedSpendTier", th.StringType)
            )),
            th.Property("tags", th.ArrayType(th.StringType)),
            th.Property("taxExempt", th.BooleanType),
            th.Property("taxExemptions", th.ArrayType(th.StringType)),
            th.Property("unsubscribeUrl", th.StringType),
            th.Property("updatedAt", th.DateTimeType),
            th.Property("validEmailAddress", th.BooleanType),
        )