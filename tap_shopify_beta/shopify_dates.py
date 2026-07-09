"""Date formatting helpers for Shopify API filters."""

import pytz


def to_shopify_utc(dt):
    """Render a datetime as an explicit UTC RFC3339 bound for Shopify filters."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=pytz.UTC)
    else:
        dt = dt.astimezone(pytz.UTC)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
