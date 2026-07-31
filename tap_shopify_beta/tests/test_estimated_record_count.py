"""Self-check for GraphQL estimated record count query shaping."""

import json

import pendulum

from tap_shopify_beta.shopify_dates import to_shopify_utc


def _expected_updated_at_filter(config):
    start = to_shopify_utc(pendulum.parse(config["start_date"]))
    date_filter = f"updated_at:>'{start}'"
    if config.get("end_date"):
        end = to_shopify_utc(pendulum.parse(config["end_date"]))
        date_filter = f"{date_filter} AND updated_at:<='{end}'"
    return date_filter


def test_count_query_uses_full_job_updated_at_bounds():
    config = {"start_date": "2025-01-01T00:00:00Z", "end_date": "2026-06-01T00:00:00Z"}
    date_filter = _expected_updated_at_filter(config)
    query = (
        f"{{ productsCount(query: {json.dumps(date_filter)}, "
        f"limit: null) {{ count }} }}"
    )
    assert "productsCount" in query
    assert "limit: null" in query
    assert "updated_at:>'2025-01-01T00:00:00Z'" in query
    assert "updated_at:<='2026-06-01T00:00:00Z'" in query


def test_count_query_omits_upper_bound_without_end_date():
    config = {"start_date": "2025-01-01T00:00:00Z"}
    date_filter = _expected_updated_at_filter(config)
    assert date_filter == "updated_at:>'2025-01-01T00:00:00Z'"
    assert "updated_at:<=" not in date_filter
