from singer_sdk import typing as th

from tap_shopify_beta.types.app import AppType
from tap_shopify_beta.types.channel_information import ChannelInformationType
from tap_shopify_beta.types.customer import CustomerType
from tap_shopify_beta.types.customer_journey_summary import CustomerJourneySummaryType
from tap_shopify_beta.types.dispute import DisputeType
from tap_shopify_beta.types.fulfillment import FulfillmentType
from tap_shopify_beta.types.mailing_address import MailingAddressType
from tap_shopify_beta.types.money_bag import MoneyBagType
from tap_shopify_beta.types.tax_line import TaxLineType

class LastOrderType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("additionalFees", th.ArrayType(th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("name", th.StringType),
                th.Property("price", MoneyBagType()),
                th.Property("taxLines", th.ArrayType(TaxLineType())),
            ))),
            th.Property("alerts", th.ArrayType(th.ObjectType(
                th.Property("actions", th.ArrayType(th.ObjectType(
                    th.Property("primary", th.BooleanType),
                    th.Property("show", th.StringType),
                    th.Property("title", th.StringType),
                    th.Property("url", th.StringType),
                ))),
                th.Property("content", th.StringType),
                th.Property("dismissibleHandle", th.StringType),
                th.Property("severity", th.StringType),
                th.Property("title", th.StringType),
            ))),
            th.Property("app", th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("name", th.StringType),
            )),
            th.Property("billingAddress", MailingAddressType()),
            th.Property("billingAddressMatchesShippingAddress", th.BooleanType),
            th.Property("cancellation", th.ObjectType(
                th.Property("staffNote", th.StringType),
            )),
            th.Property("cancelledAt", th.DateTimeType),
            th.Property("canMarkAsPaid", th.BooleanType),
            th.Property("canNotifyCustomer", th.BooleanType),
            th.Property("capturable", th.BooleanType),
            th.Property("cartDiscountAmountSet", MoneyBagType()),
            th.Property("channelInformation", ChannelInformationType()),
            th.Property("clientIp", th.StringType),
            th.Property("closed", th.BooleanType),
            th.Property("closedAt", th.DateTimeType),
            th.Property("confirmationNumber", th.StringType),
            th.Property("confirmed", th.BooleanType),
            th.Property("createdAt", th.DateTimeType),
            th.Property("currencyCode", th.StringType),
            th.Property("currentCartDiscountAmountSet", MoneyBagType()),
            th.Property("currentSubtotalLineItemsQuantity", th.IntegerType),
            th.Property("currentSubtotalPriceSet", MoneyBagType()),
            th.Property("currentTaxLines", th.ArrayType(TaxLineType())),
            th.Property("currentTotalAdditionalFeesSet", MoneyBagType()),
            th.Property("currentTotalDiscountsSet", MoneyBagType()),
            th.Property("currentTotalDutiesSet", MoneyBagType()),
            th.Property("currentTotalPriceSet", MoneyBagType()),
            th.Property("currentTotalTaxSet", MoneyBagType()),
            th.Property("currentTotalWeight", th.StringType),
            th.Property("customAttributes", th.ArrayType(th.ObjectType(
                th.Property("key", th.StringType),
                th.Property("value", th.StringType),
            ))),
            th.Property("customer", CustomerType()),
            th.Property("customerAcceptsMarketing", th.BooleanType),
            th.Property("customerJourneySummary", CustomerJourneySummaryType()),
            th.Property("customerLocale", th.StringType),
            th.Property("discountCode", th.StringType),
            th.Property("discountCodes", th.ArrayType(th.StringType)),
            th.Property("displayAddress", MailingAddressType()),
            th.Property("displayFinancialStatus", th.StringType),
            th.Property("displayFulfillmentStatus", th.StringType),
            th.Property("disputes", th.ArrayType(DisputeType())),
            th.Property("edited", th.BooleanType),
            th.Property("email", th.StringType),
            th.Property("estimatedTaxes", th.BooleanType),
            th.Property("fulfillable", th.BooleanType),
            th.Property("fulfillments", th.ArrayType(FulfillmentType())),
            th.Property("fullyPaid", th.BooleanType),
            th.Property("hasTimelineComment", th.BooleanType),
            th.Property("legacyResourceId", th.StringType),
            th.Property("merchantOfRecordApp", th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("name", th.StringType),
            )),
            th.Property("name", th.StringType),
            th.Property("netPaymentSet", MoneyBagType()),
            th.Property("note", th.StringType),
            th.Property("originalTotalAdditionalFeesSet", MoneyBagType()),
            th.Property("originalTotalDutiesSet", MoneyBagType()),
            th.Property("originalTotalPriceSet", MoneyBagType()),
            th.Property("paymentCollectionDetails", th.ObjectType(
                th.Property("additionalPaymentCollectionUrl", th.StringType),
                # th.Property("vaultedPaymentMethods", th.ArrayType( <<-- Requires read_payment_mandate access scope
                #     th.ObjectType(
                #         th.Property("id", th.StringType)
                #     )
                # )),
            )),
            th.Property("paymentGatewayNames", th.ArrayType(th.StringType)),
            th.Property("phone", th.StringType),
            th.Property("poNumber", th.StringType),
            th.Property("presentmentCurrencyCode", th.StringType),
            th.Property("processedAt", th.DateTimeType),
            th.Property("refundable", th.BooleanType),
            th.Property("requiresShipping", th.BooleanType),
            th.Property("restockable", th.BooleanType),
            th.Property("returnStatus", th.StringType),
            th.Property("sourceIdentifier", th.StringType),
            th.Property("subtotalLineItemsQuantity", th.IntegerType),
            th.Property("tags", th.ArrayType(th.StringType)),
            th.Property("taxesIncluded", th.BooleanType),
            th.Property("taxExempt", th.BooleanType),
            th.Property("test", th.BooleanType),
            th.Property("totalWeight", th.StringType),
            th.Property("unpaid", th.BooleanType),
        )
