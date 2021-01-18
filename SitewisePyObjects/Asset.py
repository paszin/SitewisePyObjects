
import boto3


class Asset:

    def __init__(self, client=boto3.client("iotsitewise"), **kwargs):


        self._client = None

    def fetch(self, client=None):
        """
        fetches and updates attributes using the sitewise api
        :param client:
        :return: success status boolean
        """
        client = client or self._client
        assert self.assetModelId
        model = client.describe_asset_model({"assetModelId": self.assetModelId})
        for k, v in model.items():
            if hasattr(self, k):
                setattr(self, k, v)
        return True


    def create(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass