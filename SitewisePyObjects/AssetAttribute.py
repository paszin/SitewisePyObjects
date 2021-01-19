import datetime
import decimal
import time
import uuid

import boto3


def get_update_entry(asset_id, property_id, value, valueType="doubleValue"):
    # convert value type
    valueType = {"INTEGER": "integerValue", "DOUBLE": "doubleValue", "BOOLEAN": "booleanValue",
                 "STRING": "stringValue"}.get(valueType, valueType)
    valueType = {int: "integerValue", float: "doubleValue", bool: "booleanValue",
                 str: "stringValue", decimal.Decimal: "doubleValue"}.get(valueType, valueType)
    return {
        "entryId": str(uuid.uuid4()),
        "assetId": asset_id,
        "propertyId": property_id,
        "propertyValues": [
            {
                "value": {
                    valueType: value,
                },
                "timestamp": {
                    "timeInSeconds": int(datetime.datetime.utcnow().timestamp()),
                    "offsetInNanos": 0
                },
                "quality": "GOOD"
            },
        ]
    }


class AssetAttribute:

    def __init__(self, assetId=None, propertyId=None, propertyAlias=None, client=boto3.client("iotsitewise")):
        self.assetId = assetId
        self.propertyId = propertyId
        self.propertyAlias = propertyAlias

        self.value = None

        self._client = client

    def __repr__(self):
        return "<{propertyId}: {value}>".format(**dict(self))

    def __iter__(self):
        keys = ["assetId", "propertyId", "propertyAlias", "value"]
        for k in keys:
            yield (k, getattr(self, k))

    def fetch(self):
        """

        :return:
        """
        # some time more attempts are needed
        attempts = 50
        while attempts > 0:
            attempts -= 1
            resp = self._client.get_asset_property_value(assetId=self.assetId, propertyId=self.propertyId)
            for dtype, v in resp.get("propertyValue", {}).get("value", {"NoneValue": None}).items():  # only one item
                self.value = v
                self.dtype = dtype
            if self.value is not None:
                break
            time.sleep(0.1)

    def update(self, value=None, dtype=None):
        """

        :param value:
        :param dtype:
        :return:
        """
        self.value = value or self.value
        entry = get_update_entry(self.assetId, self.propertyId, self.value,
                                 dtype or self.dtype or type(self.value))
        print(entry)
        response = self._client.batch_put_asset_property_value(
            entries=[entry]
        )
        return response
