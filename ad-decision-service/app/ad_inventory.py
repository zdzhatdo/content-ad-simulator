"""
Ad inventory data layer.

This module is the single source for available ads. Right now,
ad data is hardcoded in-memory, since this service is stateless and the
focus at this stage is the decision logic in main.py

All access to ad data goes through get_ad_inventory() rather than
referencing ADS directly elsewhere in the codebase. So if ad inventory later 
needs to come from a real database or a separate inventory service, 
only this function needs to change and the decision logic stays untouched.
"""

ADS = [
    {"ad_id": "ad_1", "ad_duration_seconds": 15, "region": "NJ"},
    {"ad_id": "ad_2", "ad_duration_seconds": 30, "region": "NY"},
    {"ad_id": "ad_3", "ad_duration_seconds": 30, "region": None},
]

def get_ad_inventory():
    return ADS