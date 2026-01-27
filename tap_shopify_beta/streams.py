"""Stream type classes for tap-shopify-beta."""
import abc
import copy
import json
import sys
from typing import Optional, Dict, Any, Iterable

from singer_sdk import typing as th
from singer_sdk.exceptions import RetriableAPIError
from dateutil.relativedelta import relativedelta
from pendulum import now
import requests
import urllib3
import http.client

from tap_shopify_beta.client_bulk import shopifyBulkStream
from tap_shopify_beta.client_gql import shopifyGqlStream
from tap_shopify_beta.client_rest import shopifyRestStream
from tap_shopify_beta.types.order_app import OrderAppType
from tap_shopify_beta.types.channel_information import ChannelInformationType
from tap_shopify_beta.types.customer import CustomerType
from tap_shopify_beta.types.customer_email_marketing_consent_state import CustomerEmailMarketingConsentStateType
from tap_shopify_beta.types.customer_journey_summary import CustomerJourneySummaryType
from tap_shopify_beta.types.customer_visit import CustomerVisitType
from tap_shopify_beta.types.dispute import DisputeType
from tap_shopify_beta.types.fulfillment import FulfillmentType
from tap_shopify_beta.types.image import ImageType
from tap_shopify_beta.types.last_order import LastOrderType
from tap_shopify_beta.types.line_item_node import LineItemNodeType
from tap_shopify_beta.types.count import CountType
from tap_shopify_beta.types.location import LocationType
from tap_shopify_beta.types.mergeable import MergeableType
from tap_shopify_beta.types.metafield_definition import MetafieldDefinitionType
from tap_shopify_beta.types.money_bag import MoneyBagType
from tap_shopify_beta.types.money_v2 import MoneyV2Type
from tap_shopify_beta.types.mailing_address import MailingAddressType
from tap_shopify_beta.types.company_contact import CompanyContactType
from tap_shopify_beta.types.sms_marketing_consent import SmsMarketingConsentType
from tap_shopify_beta.types.tax_line import TaxLineType

config_path = "config.json"
for i, arg in enumerate(sys.argv):
    if arg == "--config":
        if i + 1 < len(sys.argv):
            config_path = sys.argv[i + 1]
        break

with open(config_path, "r") as jsonfile:
    data = json.load(jsonfile)

stream_condition = data.get("bulk", False)
class DynamicStream(shopifyBulkStream if stream_condition else shopifyGqlStream):
    pass

class ProductsStream(DynamicStream):
    """Define product stream."""

    name = "products"
    primary_keys = ["id", "updatedAt"]
    query_name = "products"
    replication_key = "updatedAt"

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("createdAt", th.DateTimeType),
        th.Property("description", th.StringType),
        th.Property("descriptionHtml", th.StringType),
        th.Property(
            "featuredImage",
            th.ObjectType(
                th.Property("id", th.StringType), th.Property("altText", th.StringType)
            ),
        ),
        th.Property("giftCardTemplateSuffix", th.StringType),
        th.Property("handle", th.StringType),
        th.Property("hasOnlyDefaultVariant", th.BooleanType),
        th.Property("hasOutOfStockVariants", th.BooleanType),
        th.Property("isGiftCard", th.BooleanType),
        th.Property("legacyResourceId", th.StringType),
        th.Property("mediaCount", CountType()),
        th.Property("onlineStorePreviewUrl", th.StringType),
        th.Property("onlineStoreUrl", th.StringType),
        th.Property(
            "options",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("name", th.StringType),
                    th.Property("position", th.IntegerType),
                    th.Property("values", th.ArrayType(th.StringType)),
                )
            ),
        ),
        th.Property(
            "priceRangeV2",
            th.ObjectType(
                th.Property(
                    "maxVariantPrice",
                    th.ObjectType(
                        th.Property("amount", th.StringType),
                        th.Property("currencyCode", th.StringType),
                    ),
                ),
                th.Property(
                    "minVariantPrice",
                    th.ObjectType(
                        th.Property("amount", th.StringType),
                        th.Property("currencyCode", th.StringType),
                    ),
                ),
            ),
        ),
        th.Property("productType", th.StringType),
        th.Property("publishedAt", th.DateTimeType),
        th.Property("requiresSellingPlan", th.BooleanType),
        th.Property("sellingPlanGroupCount", th.IntegerType),
        th.Property(
            "seo",
            th.ObjectType(
                th.Property("title", th.StringType),
                th.Property("description", th.StringType),
            ),
        ),
        th.Property("status", th.StringType),
        th.Property("templateSuffix", th.StringType),
        th.Property("title", th.StringType),
        th.Property("totalInventory", th.IntegerType),
        th.Property("totalVariants", th.IntegerType),
        th.Property("tracksInventory", th.BooleanType),
        th.Property("updatedAt", th.DateTimeType),
        th.Property("vendor", th.StringType),
    ).to_dict()


class VariantsStream(DynamicStream):
    """Define variant stream."""

    name = "variants"
    primary_keys = ["id", "updatedAt"]
    query_name = "productVariants"
    replication_key = "updatedAt"

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("availableForSale", th.BooleanType),
        th.Property("barcode", th.StringType),
        th.Property("compareAtPrice", th.StringType),
        th.Property("createdAt", th.DateTimeType),
        th.Property("displayName", th.StringType),
        th.Property(
            "image",
            th.ObjectType(
                th.Property("id", th.StringType), th.Property("altText", th.StringType)
            ),
        ),
        th.Property("inventoryItem", th.ObjectType(th.Property("id", th.StringType))),
        th.Property("inventoryPolicy", th.StringType),
        th.Property("inventoryQuantity", th.IntegerType),
        th.Property("legacyResourceId", th.StringType),
        th.Property("position", th.IntegerType),
        th.Property("price", th.StringType),
        th.Property("product", th.ObjectType(th.Property("id", th.StringType))),
        th.Property(
            "selectedOptions",
            th.ArrayType(
                th.ObjectType(
                    th.Property("name", th.StringType),
                    th.Property("value", th.StringType),
                )
            ),
        ),
        th.Property("sellingPlanGroupCount", th.IntegerType),
        th.Property("sku", th.StringType),
        th.Property("taxable", th.BooleanType),
        th.Property("title", th.StringType),
        th.Property("updatedAt", th.DateTimeType),
    ).to_dict()


class OrdersStream(DynamicStream):
    """Define orders stream."""

    name = "orders"
    primary_keys = ["id", "updatedAt"]
    query_name = "orders"
    replication_key = "updatedAt"
    first_line_item = 250  # works as page_size for line_items
    _after_line_item = None
    last_replication_key = None
    sort_key = "UPDATED_AT"
    sort_key_type = "OrderSortKeys"

    bulk_process_fields = {
        "LineItem": "lineItems"
    }

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("app", OrderAppType()),
        th.Property("channelInformation", ChannelInformationType()),
        th.Property("billingAddress",MailingAddressType()),
        th.Property("billingAddressMatchesShippingAddress", th.BooleanType),
        th.Property("cancelledAt", th.DateTimeType),
        th.Property("cancelReason", th.StringType),
        th.Property("canMarkAsPaid", th.BooleanType),
        th.Property("canNotifyCustomer", th.BooleanType),
        th.Property("capturable", th.BooleanType),
        th.Property("cartDiscountAmountSet", MoneyBagType()),
        th.Property("clientIp", th.StringType),
        th.Property("closed", th.BooleanType),
        th.Property("closedAt", th.DateTimeType),
        th.Property("confirmed", th.BooleanType),
        th.Property("createdAt", th.DateTimeType),
        th.Property("currencyCode", th.StringType),
        th.Property("currentCartDiscountAmountSet", MoneyBagType()),
        th.Property("currentSubtotalLineItemsQuantity", th.IntegerType),
        th.Property("currentSubtotalPriceSet", MoneyBagType()),
        th.Property(
            "currentTaxLines",
            th.ArrayType(
                th.ObjectType(
                    th.Property("channelLiable", th.StringType),
                    th.Property("priceSet", MoneyBagType()),
                    th.Property("rate", th.NumberType),
                    th.Property("ratePercentage", th.NumberType),
                    th.Property("title", th.StringType),
                )
            ),
        ),
        th.Property("currentTotalDiscountsSet", MoneyBagType()),
        th.Property("currentTotalDutiesSet", MoneyBagType()),
        th.Property("currentTotalPriceSet", MoneyBagType()),
        th.Property("currentTotalTaxSet", MoneyBagType()),
        th.Property("currentTotalWeight", th.StringType),
        th.Property(
            "customer",
            th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("addresses", th.ArrayType(MailingAddressType())),
                th.Property("amountSpent", MoneyV2Type()),
                th.Property("canDelete", th.BooleanType),
                # th.Property("companyContactProfiles", th.ArrayType(CompanyContactType())),
                th.Property("createdAt", th.DateTimeType),
                th.Property("defaultAddress", MailingAddressType()),
                th.Property("displayName", th.StringType),
                th.Property("email", th.StringType),
                th.Property("emailMarketingConsent", CustomerEmailMarketingConsentStateType()),
                th.Property("firstName", th.StringType),
                th.Property("image", ImageType()),
                th.Property("lastName", th.StringType),
                # th.Property("lastOrder", LastOrderType()),
                th.Property("numberOfOrders", th.StringType),
                th.Property("note", th.StringType),
                th.Property("verifiedEmail", th.BooleanType),
                th.Property("validEmailAddress", th.BooleanType),
                th.Property("tags", th.CustomType({"type": ["array", "string"]})),
                th.Property("lifetimeDuration", th.StringType),
                th.Property("locale", th.StringType),
                th.Property("taxExempt", th.BooleanType),
                th.Property("updatedAt", th.DateTimeType),
                th.Property("smsMarketingConsent", SmsMarketingConsentType()),
            ),
        ),
        th.Property("customerId", th.StringType),
        th.Property("customerAcceptsMarketing", th.BooleanType),
        th.Property("customerLocale", th.StringType),
        th.Property("discountCode", th.StringType),
        th.Property("displayAddress", MailingAddressType()),
        th.Property("displayFinancialStatus", th.StringType),
        th.Property("displayFulfillmentStatus", th.StringType),
        th.Property("disputes",th.ArrayType(DisputeType())),
        th.Property("edited", th.BooleanType),
        th.Property("email", th.StringType),
        th.Property("estimatedTaxes", th.BooleanType),
        th.Property("fulfillable", th.BooleanType),
        th.Property("fulfillments", th.ArrayType(
            th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("inTransitAt", th.StringType),
                th.Property("legacyResourceId", th.StringType),
                th.Property("location", LocationType()),
                th.Property("name", th.StringType),
                th.Property("requiresShipping", th.BooleanType),
                th.Property("service", th.ObjectType(
                    th.Property("id", th.StringType)
                )),
                th.Property("status", th.StringType),
                th.Property("totalQuantity", th.IntegerType),
                th.Property("trackingInfo", th.ArrayType(
                    th.ObjectType(
                        th.Property("company", th.StringType),
                        th.Property("number", th.StringType),
                        th.Property("url", th.StringType),
                    ))
                ),
                th.Property("updatedAt", th.DateTimeType),
            )),
        ),
        th.Property("fullyPaid", th.BooleanType),
        th.Property("legacyResourceId", th.StringType),
        th.Property("hasTimelineComment", th.BooleanType),
        th.Property("merchantEditable", th.BooleanType),
        th.Property("name", th.StringType),
        th.Property("netPaymentSet", MoneyBagType()),
        th.Property("note", th.StringType),
        th.Property("originalTotalDutiesSet", MoneyBagType()),
        th.Property("originalTotalPriceSet", MoneyBagType()),
        th.Property("paymentGatewayNames", th.ArrayType(th.StringType)),
        th.Property("phone", th.StringType),
        th.Property("presentmentCurrencyCode", th.StringType),
        th.Property("processedAt", th.DateTimeType),
        th.Property("refundable", th.BooleanType),
        th.Property("refundDiscrepancySet", MoneyBagType()),
        th.Property(
            "refunds",
            th.ArrayType(th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("createdAt", th.DateTimeType),
                th.Property(
                    "duties",
                    th.ArrayType(th.ObjectType(
                        th.Property("amountSet", MoneyBagType()),
                    )),
                ),
                th.Property("legacyResourceId", th.StringType),
                th.Property("note", th.StringType),
                th.Property("totalRefundedSet", MoneyBagType()),
                th.Property("updatedAt", th.DateTimeType),
            ),
        )),
        th.Property("registeredSourceUrl", th.StringType),
        th.Property("requiresShipping", th.BooleanType),
        th.Property("restockable", th.BooleanType),
        th.Property("riskLevel", th.StringType),
        th.Property(
            "risks",
            th.ArrayType(
                th.ObjectType(
                    th.Property("display", th.BooleanType),
                    th.Property("level", th.StringType),
                    th.Property("message", th.StringType),
                )
            ),
        ),
        th.Property("shippingAddress", MailingAddressType()),
        th.Property(
            "shippingLine",
            th.ObjectType(
                th.Property("carrierIdentifier", th.StringType),
                th.Property("code", th.StringType),
                th.Property("custom", th.BooleanType),
            ),
        ),
        th.Property("subtotalLineItemsQuantity", th.IntegerType),
        th.Property("subtotalPriceSet", MoneyBagType()),
        th.Property("taxesIncluded", th.BooleanType),
        th.Property(
            "taxLines",
            th.ArrayType(
                th.ObjectType(
                    th.Property("channelLiable", th.BooleanType),
                    th.Property("priceSet", MoneyBagType()),
                    th.Property("rate", th.NumberType),
                    th.Property("ratePercentage", th.NumberType),
                    th.Property("title", th.StringType),
                )
            ),
        ),
        th.Property("totalCapturableSet", MoneyBagType()),
        th.Property("totalDiscountsSet", MoneyBagType()),
        th.Property("totalOutstandingSet", MoneyBagType()),
        th.Property("totalPriceSet", MoneyBagType()),
        th.Property("totalReceivedSet", MoneyBagType()),
        th.Property("totalRefundedSet", MoneyBagType()),
        th.Property("totalRefundedShippingSet", MoneyBagType()),
        th.Property("totalShippingPriceSet", MoneyBagType()),
        th.Property("totalTaxSet", MoneyBagType()),
        th.Property("totalTipReceivedSet", MoneyBagType()),
        th.Property("totalWeight", th.StringType),
        th.Property(
            "transactions",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("accountNumber", th.StringType),
                    th.Property("amountSet", MoneyBagType()),
                    th.Property("authorizationCode", th.StringType),
                    th.Property("authorizationExpiresAt", th.DateTimeType),
                    th.Property("createdAt", th.DateTimeType),
                    th.Property("errorCode", th.StringType),
                    th.Property(
                        "fees",
                        th.ArrayType(
                            th.ObjectType(
                                th.Property("amount", MoneyV2Type()),
                                th.Property("flatFee", MoneyV2Type()),
                                th.Property("flatFeeName", th.StringType),
                                th.Property("id", th.StringType),
                                th.Property("rate", th.StringType),
                                th.Property("rateName", th.StringType),
                                th.Property("taxAmount", MoneyV2Type()),
                                th.Property("type", th.StringType),
                            )
                        ),
                    ),
                    th.Property("formattedGateway", th.StringType),
                    th.Property("gateway", th.StringType),
                    th.Property("kind", th.StringType),
                    th.Property("manuallyCapturable", th.BooleanType),
                    th.Property("maximumRefundableV2", MoneyV2Type()),
                    th.Property("multiCapturable", th.BooleanType),
                    th.Property("order", th.ObjectType(
                        th.Property("id", th.StringType)
                    )),
                    th.Property("parentTransaction", th.ObjectType(
                        th.Property("id", th.StringType)
                    )),
                    th.Property("paymentIcon", ImageType()),
                    th.Property("paymentId", th.StringType),
                    th.Property("processedAt", th.DateTimeType),
                    th.Property("receiptJson", th.StringType),
                    th.Property("settlementCurrency", th.StringType),
                    th.Property("settlementCurrencyRate", th.StringType),
                    th.Property("status", th.StringType),
                    th.Property("test", th.BooleanType),
                    th.Property("totalUnsettledSet", MoneyBagType()),
                    # th.Property("user", th.ObjectType( ->> Needs read_users access scope
                    #     th.Property("id", th.StringType)
                    # )),
                )
            ),
        ),
        th.Property("unpaid", th.BooleanType),
        th.Property("updatedAt", th.DateTimeType),
        th.Property("sourceIdentifier", th.StringType),
        th.Property("lineItems", th.ArrayType(LineItemNodeType())), #
    ).to_dict()

    def has_next_page_line_items(self, record):
        return record.get("lineItems", {}).get("pageInfo", {}).get("hasNextPage", False)

    def parse_response(self, response):
        records = super().parse_response(response)
        # iterate through lines pages
        decorated_request = self.request_decorator(self._request)
        for record in records:
            if self.config.get("bulk", False):
                yield record
                continue

            # paginate through lineItems for non bulk requests
            context = {"order_id": record["id"].split("/")[-1]}
            line_items_edges = record.get("lineItems", {}).get("edges", [])
            has_next_page = self.has_next_page_line_items(record)
            order_node = record
            while has_next_page:
                self.after_line_item = "\"" + order_node.get("lineItems", {}).get("edges", [])[-1].get("cursor") + "\""
                prepared_request = self.prepare_request(
                    context, next_page_token=None
                )
                resp = decorated_request(prepared_request, context)
                orders = resp.json().get('data', {}).get('orders',{}).get('edges',[])
                if len(orders) > 1:
                    self.logger.warning(f"More than one order with same id. id={context['order_id']} and orders={orders}")
                order_node = orders[0].get('node')
                line_items_edges.extend(order_node.get("lineItems", {}).get("edges", []))
                has_next_page = self.has_next_page_line_items(order_node)
            record["lineItems"] = [edge.get("node") for edge in line_items_edges]

            is_customer_id_selected = 'customerId' in self.selected_properties
            customer = record.get('customer')
            if is_customer_id_selected and isinstance(customer, dict):
                record['customerId'] = customer.get('id')

            self.after_line_item = None
            if record.get(self.replication_key):
                self.last_replication_key = max(self.last_replication_key, record.get(self.replication_key)) if self.last_replication_key else record.get(self.replication_key)
            elif self.last_replication_key:
                record[self.replication_key] = self.last_replication_key
            else:
                raise Exception(f"No replication key in this record and no replication key could be set for it. id={record['id']}. record={record}")
            yield record

    @property
    def after_line_item(self):
        return self._after_line_item

    @after_line_item.setter
    def after_line_item(self, value):
        self._after_line_item = value
        # Clear the cached query when after_line_item changes
        self._clear_cache()

    def _clear_cache(self):
        # Clear the cache of the query
        if 'query' in self.__dict__:
            del self.__dict__['query']

    def get_url_params_line_items(self, context, next_page_token):
        """Return a dictionary of values to be used in URL parameterization."""
        params = {
            "first": 1,
            "filter": f"id:{context['order_id']}",
        }
        return params

    def prepare_request_payload(self, context, next_page_token):
        """Prepare the data payload for the GraphQL API request."""
        if context and "order_id" in context:
            params = self.get_url_params_line_items(context, next_page_token)
        else:
            params = self.get_url_params(context, next_page_token)
        query = self.query.lstrip()

        if 'customerId' in query:        
            if 'customer {' in query:
                query = query.replace("customerId", "")
            else:
                query = query.replace("customerId", "customer { id }")

        request_data = {
            "query": (" ".join([line.strip() for line in query.splitlines()])),
            "variables": params,
        }
        # self.logger.info(f"Attempting request with variables {params} and query: {request_data['query']}")
        return request_data

class ShopStream(shopifyGqlStream):
    """Define shop stream."""

    name = "shop"
    primary_keys = ["id"]
    query_name = "shop"
    replication_key = None
    is_list = False

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("contactEmail", th.StringType),
        th.Property(
            "countriesInShippingZones",
            th.ObjectType(
                th.Property("countryCodes", th.ArrayType(th.StringType)),
            ),
            th.Property("includeRestOfWorld", th.BooleanType),
        ),
        th.Property("currencyCode", th.StringType),
        th.Property(
            "currencyFormats",
            th.ObjectType(
                th.Property("moneyFormat", th.StringType),
                th.Property("moneyInEmailsFormat", th.StringType),
                th.Property("moneyWithCurrencyFormat", th.StringType),
                th.Property("moneyWithCurrencyInEmailsFormat", th.StringType),
            ),
        ),
        th.Property("customerAccounts", th.StringType),
        th.Property("description", th.StringType),
        th.Property(
            "domains",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("host", th.StringType),
                    th.Property("sslEnabled", th.BooleanType),
                    th.Property("url", th.StringType),
                )
            ),
        ),
        th.Property("email", th.StringType),
        th.Property("enabledPresentmentCurrencies", th.ArrayType(th.StringType)),
        th.Property(
            "features",
            th.ObjectType(
                th.Property("branding", th.StringType),
                th.Property("captcha", th.BooleanType),
                th.Property("captchaExternalDomains", th.BooleanType),
                th.Property("dynamicRemarketing", th.BooleanType),
                th.Property("giftCards", th.BooleanType),
                th.Property("harmonizedSystemCode", th.BooleanType),
                th.Property("internationalDomains", th.BooleanType),
                th.Property("internationalPriceOverrides", th.BooleanType),
                th.Property("internationalPriceRules", th.BooleanType),
                th.Property("reports", th.BooleanType),
                th.Property("sellsSubscriptions", th.BooleanType),
                th.Property("showMetrics", th.BooleanType),
            ),
        ),
        th.Property(
            "fulfillmentServices",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("callbackUrl", th.StringType),
                    th.Property("fulfillmentOrdersOptIn", th.BooleanType),
                    th.Property("handle", th.StringType),
                    th.Property("inventoryManagement", th.BooleanType),
                    th.Property("location", LocationType()),
                    th.Property("serviceName", th.StringType),
                    th.Property("type", th.StringType),
                )
            ),
        ),
        th.Property("ianaTimezone", th.StringType),
        th.Property(
            "limitedPendingOrderCount",
            th.ObjectType(
                th.Property("atMax", th.BooleanType),
                th.Property("count", th.IntegerType),
            ),
        ),
        th.Property("myshopifyDomain", th.StringType),
        th.Property("name", th.StringType),
        th.Property(
            "navigationSettings",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("title", th.StringType),
                    th.Property("url", th.StringType),
                )
            ),
        ),
        th.Property("orderNumberFormatPrefix", th.StringType),
        th.Property("orderNumberFormatSuffix", th.StringType),
        th.Property(
            "navigationSettings",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("title", th.StringType),
                    th.Property("url", th.StringType),
                )
            ),
        ),
        th.Property(
            "primaryDomain",
            th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("host", th.StringType),
                th.Property("sslEnabled", th.BooleanType),
                th.Property("url", th.StringType),
            ),
        ),
        th.Property("taxesIncluded", th.BooleanType),
        th.Property("taxShipping", th.BooleanType),
        th.Property("timezoneAbbreviation", th.StringType),
        th.Property("timezoneOffset", th.StringType),
        th.Property("timezoneOffsetMinutes", th.IntegerType),
        th.Property("unitSystem", th.StringType),
        th.Property("url", th.StringType),
        th.Property("weightUnit", th.StringType),
    ).to_dict()


class InventoryItemsStream(DynamicStream):
    """Define Intentory Items stream."""

    name = "inventory_items"
    primary_keys = ["id"]
    query_name = "inventoryItems"
    replication_key = "updatedAt"

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("countryCodeOfOrigin", th.StringType),
        th.Property("createdAt", th.DateTimeType),
        th.Property("duplicateSkuCount", th.IntegerType),
        th.Property("harmonizedSystemCode", th.StringType),
        th.Property("inventoryHistoryUrl", th.StringType),
        th.Property("legacyResourceId", th.StringType),
        th.Property("locationsCount", CountType()),
        th.Property("provinceCodeOfOrigin", th.StringType),
        th.Property("requiresShipping", th.BooleanType),
        th.Property("sku", th.StringType),
        th.Property("tracked", th.BooleanType),
        th.Property(
            "trackedEditable",
            th.ObjectType(
                th.Property("locked", th.BooleanType),
                th.Property("reason", th.StringType),
            ),
        ),
        th.Property(
            "unitCost",
            th.ObjectType(
                th.Property("amount", th.StringType),
                th.Property("currencyCode", th.StringType),
            ),
        ),
        th.Property("updatedAt", th.DateTimeType),
        th.Property(
            "variant",
            th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("availableForSale", th.BooleanType),
                th.Property("barcode", th.StringType),
                th.Property("compareAtPrice", th.StringType),
                th.Property("createdAt", th.DateTimeType),
                th.Property("defaultCursor", th.StringType),
                th.Property("displayName", th.StringType),
                th.Property("inventoryPolicy", th.StringType),
                th.Property(
                    "image",
                    th.ObjectType(
                        th.Property("id", th.StringType),
                        th.Property("altText", th.StringType),
                    ),
                ),
                th.Property("inventoryQuantity", th.IntegerType),
                th.Property("legacyResourceId", th.StringType),
                th.Property("position", th.IntegerType),
                th.Property("price", th.StringType),
                th.Property(
                    "selectedOptions",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property("name", th.StringType),
                            th.Property("value", th.StringType),
                        )
                    ),
                ),
                th.Property("sku", th.StringType),
                th.Property("taxCode", th.StringType),
                th.Property("taxable", th.BooleanType),
                th.Property("title", th.StringType),
                th.Property("updatedAt", th.DateTimeType),
            ),
        ),
    ).to_dict()


class CollectionsStream(DynamicStream):
    """Define collections stream."""

    name = "collections"
    primary_keys = ["id"]
    query_name = "collections"
    replication_key = "updatedAt"

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("description", th.StringType),
        th.Property("descriptionHtml", th.StringType),
        th.Property("handle", th.StringType),
        th.Property(
            "image",
            th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("altText", th.StringType)
            ),
        ),
        th.Property("legacyResourceId", th.StringType),
        th.Property("productsCount", CountType()),
        th.Property("sortOrder", th.StringType),
        th.Property("templateSuffix", th.StringType),
        th.Property("title", th.StringType),
        th.Property("updatedAt", th.DateTimeType),
    ).to_dict()


class CustomersStream(DynamicStream):
    """Define collections stream."""

    name = "customers"
    primary_keys = ["id"]
    query_name = "customers"
    replication_key = "updatedAt"
    sort_key = "UPDATED_AT"
    sort_key_type = "CustomerSortKeys"

    """
        Access denied for companyContactProfiles field.
        Required access: `read_customers` access scope or `read_companies` access scope.
        Also: The API client must be installed on a Shopify Plus store.
    """
    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("firstName", th.StringType),
        th.Property("lastName", th.StringType),
        th.Property("email", th.StringType),
        th.Property("phone", th.StringType),
        th.Property("numberOfOrders", th.StringType),
        th.Property("amountSpent", MoneyV2Type()),
        # th.Property("companyContactProfiles", th.ArrayType(CompanyContactType())), # -> For some clients, we see "NO ACCESS" error,added complete error above.
        th.Property("multipassIdentifier", th.StringType),
        th.Property("note", th.StringType),
        th.Property("verifiedEmail", th.BooleanType),
        th.Property("validEmailAddress", th.BooleanType),
        th.Property("tags", th.CustomType({"type": ["array", "string"]})),
        th.Property("lifetimeDuration", th.StringType),
        th.Property("legacyResourceId", th.StringType),
        th.Property("taxExempt", th.BooleanType),
        th.Property("defaultAddress", MailingAddressType()),
        th.Property("lastOrder", LastOrderType()),
        th.Property("addresses", th.ArrayType(MailingAddressType())),
        th.Property("image", ImageType()),
        th.Property("canDelete", th.BooleanType),
        th.Property("createdAt", th.DateTimeType),
        th.Property("updatedAt", th.DateTimeType),
        th.Property("emailMarketingConsent", CustomerEmailMarketingConsentStateType()),
        th.Property("smsMarketingConsent", SmsMarketingConsentType()),
        th.Property("mergeable", MergeableType()),
    ).to_dict()


class LocationsStream(shopifyRestStream):
    """Define collections stream."""

    path = "locations.json"
    name = "locations"
    primary_keys = ["id"]
    replication_key = None
    records_jsonpath = "$.locations.[*]"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("address1", th.StringType),
        th.Property("address2", th.StringType),
        th.Property("city", th.StringType),
        th.Property("zip", th.StringType),
        th.Property("province", th.StringType),
        th.Property("country", th.StringType),
        th.Property("phone", th.StringType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
        th.Property("country_code", th.StringType),
        th.Property("country_name", th.StringType),
        th.Property("province_code", th.StringType),
        th.Property("legacy", th.BooleanType),
        th.Property("active", th.BooleanType),
        th.Property("admin_graphql_api_id", th.StringType),
        th.Property("localized_country_name", th.StringType),
        th.Property("localized_province_name", th.StringType),
    ).to_dict()

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "location_id": record["id"],
        }


class InventoryLevelRestStream(shopifyRestStream):
    """Define collections stream."""

    path = "inventory_levels.json"
    name = "inventory_level_rest"
    primary_keys = ["id"]
    records_jsonpath = "$.inventory_levels.[*]"

    @property
    def add_params(self):
        location_id = self.tap_state.get("bookmarks").get("inventory_level_rest").get("partitions")[-1]["context"]["location_id"]
        params = {"location_ids": location_id}
        if self.config.get("inventory_item_ids"):
            item_ids = self.config.get("inventory_item_ids")
            if isinstance(item_ids,list):
                item_ids = ",".join(item_ids)
            params.update({"inventory_item_ids":item_ids})
        return params

    parent_stream_type = LocationsStream

    schema = th.PropertiesList(
        th.Property("admin_graphql_api_id", th.StringType),
    ).to_dict()

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "inventory_level_id": record["admin_graphql_api_id"],
        }


class InventoryLevelGqlStream(shopifyGqlStream):
    """Define collections stream."""

    name = "inventory_level_gql"
    primary_keys = ["id"]
    replication_key = None
    parent_stream_type = InventoryLevelRestStream
    query_name = "inventoryLevel"
    is_list = False
    # change needed as incoming and available fields are deprecated in inventory_level
    additional_arguments = {
        "quantities": '(names: ["available", "incoming"])'
    }

    @property
    def single_object_params(self):
        inventory_level_id = self.tap_state.get("bookmarks").get("inventory_level_gql").get("partitions")[0]["context"]["inventory_level_id"]
        return {"id": inventory_level_id}

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("quantities", th.ArrayType(
            th.ObjectType(
                th.Property("name", th.StringType),
                th.Property("quantity", th.IntegerType),
            )
        )),
        th.Property("item", th.ObjectType(
            th.Property("id", th.StringType),
            th.Property("sku", th.StringType),
        )),
        th.Property("location", th.ObjectType(
            th.Property("id", th.StringType),
            th.Property("name", th.StringType),
        )),
    ).to_dict()


class PriceRulesStream(shopifyRestStream):
    """Define collections stream."""

    name = "price_rules"
    primary_keys = ["id"]
    replication_key = "updated_at"
    records_jsonpath = "$.price_rules.[*]"
    path = "price_rules.json"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("value_type", th.StringType),
        th.Property("value", th.StringType),
        th.Property("customer_selection", th.StringType),
        th.Property("target_type", th.StringType),
        th.Property("target_selection", th.StringType),
        th.Property("allocation_method", th.StringType),
        th.Property("allocation_limit", th.StringType),
        th.Property("once_per_customer", th.BooleanType),
        th.Property("usage_limit", th.IntegerType),
        th.Property("starts_at", th.DateTimeType),
        th.Property("ends_at", th.DateTimeType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
        th.Property("entitled_product_ids", th.ArrayType(th.IntegerType)),
        th.Property("entitled_variant_ids", th.ArrayType(th.IntegerType)),
        th.Property("entitled_collection_ids", th.ArrayType(th.IntegerType)),
        th.Property("entitled_country_ids", th.ArrayType(th.IntegerType)),
        th.Property("prerequisite_product_ids", th.ArrayType(th.IntegerType)),
        th.Property("prerequisite_variant_ids", th.ArrayType(th.IntegerType)),
        th.Property("prerequisite_collection_ids", th.ArrayType(th.IntegerType)),
        th.Property("prerequisite_saved_search_ids", th.ArrayType(th.IntegerType)),
        th.Property("customer_segment_prerequisite_ids", th.ArrayType(th.IntegerType)),
        th.Property("prerequisite_customer_ids", th.ArrayType(th.IntegerType)),
        th.Property("prerequisite_subtotal_range", th.StringType),
        th.Property("prerequisite_quantity_range", th.ObjectType(
            th.Property("greater_than_or_equal_to", th.IntegerType)
        )),
        th.Property("prerequisite_shipping_price_range", th.ObjectType(
            th.Property("less_than_or_equal_to", th.IntegerType)
        )),
        th.Property("prerequisite_to_entitlement_quantity_ratio", th.ObjectType(
            th.Property("prerequisite_quantity", th.StringType),
            th.Property("entitled_quantity", th.IntegerType),
        )),
        th.Property("prerequisite_to_entitlement_purchase", th.ObjectType(
            th.Property("prerequisite_amount", th.StringType),
        )),
        th.Property("prerequisite_subtotal_range", th.ObjectType(
            th.Property("greater_than_or_equal_to", th.StringType),
        )),
        th.Property("title", th.StringType),
        th.Property("_sdc_shop_myshopify_domain", th.StringType),
        th.Property("_sdc_shop_id", th.IntegerType),
        th.Property("_sdc_shop_name", th.StringType),
        th.Property("admin_graphql_api_id", th.StringType),
    ).to_dict()


class EventProductsStream(shopifyRestStream):
    """Define collections stream."""

    name = "event_products"
    primary_keys = ["id"]
    replication_key = "created_at"
    records_jsonpath = "$.events.[*]"
    path = "events.json"
    _current_date_range: Optional[Dict[str, Any]] = None

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("subject_id", th.IntegerType),
        th.Property("created_at", th.DateTimeType),
        th.Property("subject_type", th.StringType),
        th.Property("verb", th.StringType),
        th.Property("arguments", th.ArrayType(th.CustomType({"type": ["number", "string", "null", "object"]}))),
        th.Property("body", th.StringType),
        th.Property("message", th.StringType),
        th.Property("author", th.StringType),
        th.Property("description", th.StringType),
        th.Property("path", th.StringType),
    ).to_dict()

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        
        # Get base params from parent
        params = super().get_url_params(context, next_page_token)
        
        # If there's no next_page_token, and a date range set (from monthly chunking), override date params
        if not next_page_token and self._current_date_range:
            start_date = self._current_date_range["start"]
            end_date = self._current_date_range["end"]
            rep_key_param_min = f"{self.replication_key}_min"
            rep_key_param_max = f"{self.replication_key}_max"
            params[rep_key_param_min] = start_date.strftime('%Y-%m-%dT%H:%M:%S.%f')
            params[rep_key_param_max] = end_date.strftime('%Y-%m-%dT%H:%M:%S.%f')
        
        return params

    def custom_request_records(self, context: Optional[dict], use_backoff: bool = True) -> Iterable[dict]:
        """Same as the RESTStream's request_records, but with option to use backoff or not."""
        next_page_token: Any = None
        finished = False
        if use_backoff:
            decorated_request = self.request_decorator(self._request)
        else:
            decorated_request = self._request

        while not finished:
            prepared_request = self.prepare_request(
                context, next_page_token=next_page_token
            )
            resp = decorated_request(prepared_request, context)
            yield from self.parse_response(resp)
            previous_token = copy.deepcopy(next_page_token)
            next_page_token = self.get_next_page_token(
                response=resp, previous_token=previous_token
            )
            if next_page_token and next_page_token == previous_token:
                raise RuntimeError(
                    f"Loop detected in pagination. "
                    f"Pagination token {next_page_token} is identical to prior token."
                )
            # Cycle until get_next_page_token() no longer returns a value
            finished = not next_page_token

    def request_records(self, context: Optional[dict]) -> Iterable[dict]:
        """Request records from REST endpoint(s), using chunking as fallback if normal request fails.
        
        This method first tries the normal request without backoff. If it fails with HTTP/network errors
        (RetriableAPIError, RequestException, etc.), it falls back to splitting the date range into 
        1-month intervals and processing each separately with backoff enabled.
        """
        # First, try the normal request without backoff
        try:
            yield from self.custom_request_records(context, use_backoff=False)
            return
        except (RetriableAPIError, requests.exceptions.RequestException, 
                urllib3.exceptions.HTTPError, http.client.HTTPException) as e:
            self.logger.info(f"Received error: {e}, falling back to chunked date range processing")
        
        # Fallback: Split into monthly chunks
        start_date = self.get_starting_time(context)
        if not start_date:
            raise e  # Re-raise the original exception if we can't chunk
        
        current_date = now()
        
        # Split into monthly chunks
        chunk_start = start_date
        while chunk_start < current_date:
            # Calculate chunk end (1 month from start)
            chunk_end = chunk_start + relativedelta(months=1)
            self.logger.info(f"Processing chunk from {chunk_start} to {chunk_end}")

            self._current_date_range = {
                "start": chunk_start,
                "end": chunk_end
            }

            # Process this chunk using custom_request_records
            yield from self.custom_request_records(context)
            
            # Move to next month
            chunk_start = chunk_end


class MarketingEventsStream(shopifyRestStream):
    """Define collections stream."""

    name = "marketing_events"
    primary_keys = ["id"]
    path = "marketing_events.json"
    records_jsonpath= "$.marketing_events.[*]"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("event_type", th.StringType),
        th.Property("remote_id", th.StringType),
        th.Property("started_at", th.DateTimeType),
        th.Property("ended_at", th.DateTimeType),
        th.Property("scheduled_to_end_at", th.DateTimeType),
        th.Property("budget", th.NumberType),
        th.Property("currency", th.StringType),
        th.Property("manage_url", th.StringType),
        th.Property("preview_url", th.StringType),
        th.Property("utm_campaign", th.StringType),
        th.Property("utm_source", th.StringType),
        th.Property("utm_medium", th.StringType),
        th.Property("budget_type", th.StringType),
        th.Property("description", th.StringType),
        th.Property("marketing_channel", th.StringType),
        th.Property("paid", th.BooleanType),
        th.Property("referring_domain", th.StringType),
        th.Property("breadcrumb_id", th.IntegerType),
        th.Property("marketing_activity_id", th.IntegerType),
        th.Property("admin_graphql_api_id", th.StringType),
        th.Property("marketed_resources", th.ArrayType(
            th.ObjectType(
                th.Property("type", th.StringType),
                th.Property("id", th.IntegerType),
            )
        )),
    ).to_dict()


class EventDestroyedProductsStream(EventProductsStream):
    """Define collections stream."""

    name = "event_destroyed_products"
    add_params = {"verb": "destroy"}


class CustomerVisitStream(shopifyGqlStream, metaclass=abc.ABCMeta):
    """Define base class for CustomerVisit stream"""

    primary_keys = ["id", "updatedAt"]
    query_name = "orders"
    replication_key = "updatedAt"
    page_size = 100
    is_timestamp_replication_key = True
    json_path = "$.edges[*].node"  # JSONPath to compile over the result of filter_response()
    sort_key = "UPDATED_AT"
    sort_key_type = "OrderSortKeys"

    @property
    def schema(self):
        return th.PropertiesList(
            th.Property("id", th.StringType),
            th.Property("updatedAt", th.DateTimeType),
            th.Property("customerJourneySummary", th.ObjectType(
                th.Property(self.visit_type, CustomerVisitType())
            ))
        ).to_dict()

    def filter_response(self, response_json: dict) -> dict:
        return {
            'edges': [
                e
                for e in response_json['data']['orders']['edges']
                if e.get('node',{}).get('customerJourneySummary',{}).get(self.visit_type)
            ]
        }

class CustomerFirstVisitStream(CustomerVisitStream):
    """Define Customer Visit stream"""

    name = "customer_first_visit"

    @property
    def visit_type(self) -> str:
        return "firstVisit"

class CustomerLastVisitsStream(CustomerVisitStream):
    """Define Customer Visit stream"""

    name = "customer_last_visit"

    @property
    def visit_type(self) -> str:
        return "lastVisit"


class CustomerJourneySummaryStream(shopifyGqlStream):
    """Define base class for CustomerVisit stream"""

    name = "customer_journey_summary"
    primary_keys = ["id", "updatedAt"]
    query_name = "orders"
    replication_key = "updatedAt"
    page_size = 100
    is_timestamp_replication_key = True
    sort_key = "UPDATED_AT"
    sort_key_type = "OrderSortKeys"

    schema = th.PropertiesList(
            th.Property("id", th.StringType),
            th.Property("updatedAt", th.DateTimeType),
            th.Property("customerJourneySummary", th.ObjectType(
                th.Property("customerOrderIndex", th.IntegerType),
                th.Property("daysToConversion", th.IntegerType),
                th.Property("firstVisit", CustomerVisitType()),
                th.Property("lastVisit", CustomerVisitType()),
                th.Property("momentsCount", CountType()),
                th.Property("ready", th.BooleanType),
            ))
    ).to_dict()
