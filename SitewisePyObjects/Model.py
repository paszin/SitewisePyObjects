
import boto3


class Model:

    def __init__(self, client=boto3.client("iotsitewise"), **kwargs):
        self.assetModelId = kwargs.get("assetModelId")
        self.assetModelArn =  kwargs.get("assetModelArn")
        self.assetModelName =  kwargs.get("assetModelName")
        self.assetModelDescription =  kwargs.get("assetModelDescription")
        self.assetModelProperties =  kwargs.get("assetModelProperties", [])
        self.assetModelHierarchies =  kwargs.get("assetModelHierarchies", [])
        self.assetModelCompositeModels =  kwargs.get("assetModelCompositeModels", [])
        self.assetModelCreationDate = None
        self.assetModelLastUpdateDate = None
        self.assetModelStatus = None

        self._client = client

        self._repr_template = "<Model: {assetModelName} - {assetModelId}>"

    def __repr__(self):
        return self._repr_template.format(**dict(self))

    def __iter__(self):
        keys = ["assetModelId", "assetModelArn", "assetModelName", "assetModelDescription", "assetModelProperties", "assetModelHierarchies", "assetModelCompositeModels"]
        for k in keys:
            yield (k, getattr(self, k))


    def fetch(self, client=None):
        """
        fetches and updates attributes using the sitewise api
        :param client:
        :return: success status boolean
        """
        client = client or self._client
        assert self.assetModelId
        model = client.describe_asset_model(assetModelId=self.assetModelId)
        for k, v in model.items():
            if hasattr(self, k):
                setattr(self, k, v)
        return True


    def create(self, client=None):
        """

        :param client:
        :return:
        """
        client = client or self._client
        required_keys = ["assetModelName", "assetModelDescription", "assetModelProperties", "assetModelHierarchies", "assetModelCompositeModels"]
        kwargs = {k: getattr(self, k) for k in required_keys}
        resp = client.create_asset_model(**kwargs)
        self.assetModelId = resp["assetModelId"]
        self.assetModelArn = resp["assetModelArn"]
        self.assetModelStatus = resp["assetModelStatus"]
        return True


    def delete(self, client=None):
        """

        :param client:
        :return:
        """
        client = client or self._client
        assert self.assetModelId
        response = client.delete_asset_model(
            assetModelId=self.assetModelId
        )
        return response

    def update(self):
        pass