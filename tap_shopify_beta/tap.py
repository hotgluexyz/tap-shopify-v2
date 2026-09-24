"""shopify-beta tap class."""

from typing import Any, List, Optional

from hotglue_singer_sdk import Stream, Tap
from hotglue_singer_sdk import typing as th

from tap_shopify_beta.auth import ShopifyOAuthAuthenticator, shopify_oauth_token_url
from tap_shopify_beta.streams import (
    CollectionsStream,
    CustomersStream,
    CustomerJourneySummaryStream,
    CustomerFirstVisitStream,
    CustomerLastVisitsStream,
    InventoryItemsStream,
    OrdersStream,
    ProductsStream,
    ShopStream,
    VariantsStream,
    LocationsStream,
    InventoryLevelRestStream,
    InventoryLevelGqlStream,
    PriceRulesStream,
    EventProductsStream,
    EventDestroyedProductsStream,
    MarketingEventsStream,
    FulfillmentsStream,
    RefundsStream,
    PayoutsStream
)

STREAM_TYPES = [
    ProductsStream,
    VariantsStream,
    ShopStream,
    OrdersStream,
    InventoryItemsStream,
    CollectionsStream,
    CustomersStream,
    CustomerJourneySummaryStream,
    CustomerFirstVisitStream,
    CustomerLastVisitsStream,
    LocationsStream,
    InventoryLevelRestStream,
    InventoryLevelGqlStream,
    PriceRulesStream,
    EventProductsStream,
    EventDestroyedProductsStream,
    MarketingEventsStream,
    FulfillmentsStream,
    RefundsStream,
    PayoutsStream
]


class TapshopifyBeta(Tap):
    """shopify-beta tap class."""

    name = "tap-shopify-beta"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_key",
            th.StringType,
            required=False,
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "shop", th.StringType, required=True, description="Shopify string name"
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
        ),
        th.Property(
            "end_date",
            th.DateTimeType,
            description="The latest record date to sync (inclusive)",
        ),
        th.Property(
            "client_id",
            th.StringType,
            required=False,
            description="Shopify app API key (OAuth client id)",
        ),
        th.Property(
            "client_secret",
            th.StringType,
            required=False,
            description="Shopify app API secret",
        ),
        th.Property(
            "access_token",
            th.StringType,
            required=False,
            description="Shopify Admin API access token from OAuth",
        ),
        th.Property(
            "refresh_token",
            th.StringType,
            required=False,
            description="Shopify OAuth refresh token for expiring offline tokens",
        ),
        th.Property(
            "expires_in",
            th.IntegerType,
            required=False,
            description="Access token lifetime in seconds or absolute expiry epoch after refresh",
        ),
        th.Property(
            "refresh_token_expires_in",
            th.IntegerType,
            required=False,
            description="Refresh token lifetime in seconds from Shopify",
        ),
        th.Property(
            "redirect_uri",
            th.StringType,
            required=False,
            description="OAuth redirect URI registered for the Shopify app",
        ),
    ).to_dict()

    @classmethod
    def access_token_support(cls, connector: Optional[Any] = None):
        """Authenticator and token URL for the ``--access-token`` CLI.

        The SDK calls this with no ``connector`` to detect support; we return a
        placeholder endpoint because ``shop`` is not available yet. When
        ``connector.config`` includes ``shop``, the URL is built for that store
        (the path used for real refresh runs).
        """
        if connector is None or not (connector.config or {}).get("shop"):
            auth_endpoint = "https://{shop}.myshopify.com/admin/oauth/access_token"
        else:
            auth_endpoint = shopify_oauth_token_url(connector.config)
        return (ShopifyOAuthAuthenticator, auth_endpoint)

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]


if __name__ == "__main__":
    TapshopifyBeta.cli()
