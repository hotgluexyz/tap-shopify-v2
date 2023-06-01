"""shopify-beta tap class."""

from typing import List

from singer_sdk import Stream, Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_shopify_beta.streams import (
    CollectionsStream,
    CustomersStream,
    InventoryItemsStream,
    OrdersStream,
    ProductsStream,
    ShopStream,
    VariantsStream,
    LocationsStream,
    InventoryLevelRestStream,
    InventoryLevelGqlStream
)

STREAM_TYPES = [
    ProductsStream,
    VariantsStream,
    ShopStream,
    OrdersStream,
    InventoryItemsStream,
    CollectionsStream,
    CustomersStream,
    LocationsStream,
    InventoryLevelRestStream,
    InventoryLevelGqlStream
]


class TapshopifyBeta(Tap):
    """shopify-beta tap class."""

    name = "tap-shopify-beta"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_key",
            th.StringType,
            required=True,
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
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]


if __name__ == "__main__":
    TapshopifyBeta.cli()
