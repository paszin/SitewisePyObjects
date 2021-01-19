import time

import boto3

from .AssetAttribute import AssetAttribute


class Asset:

    def __init__(self, client=boto3.client("iotsitewise"), **kwargs):

        self.assetId = kwargs.get("assetId")
        self.assetArn = kwargs.get("assetArn")
        self.assetName = kwargs.get("assetName")
        self.assetModelId = kwargs.get("assetModelId")
        self.assetProperties = kwargs.get("assertProperties", [])
        self.assetHierarchies = kwargs.get("assetHierarchies", [])
        self.assetCompositeModels = kwargs.get("assetCompositeModels", [])
        self.assetCreationDate = kwargs.get("assetCreationDate")
        self.assetLastUpdateDate = kwargs.get("assetLastUpdateDate")
        self.assetStatus = kwargs.get("assetStatus")

        # these attributes are derived from the describe response and consts of specific objects
        self._model = None
        self._attributes = None
        self.measurements = None
        self.transforms = None
        self.metrics = None
        self.associated_assets = None

        self._client = client

        self._repr_template = "<Asset: {assetName}>"

    def __repr__(self):
        return self._repr_template.format(**dict(self))

    def __iter__(self):
        keys = ["assetId", "assetArn", "assetName", "assetModelId", "assetProperties", "assetHierarchies",
                "assetCompositeModels"]
        for k in keys:
            yield (k, getattr(self, k))

    @staticmethod
    def fetch_by_name(assetName, assetModelId=None, client=boto3.client("iotsitewise")):
        """
        If no assetModelId provided, the asset must be a top level asset
        :param assetName: Name of the model
        :param assetModelId: assetModelId
        :param client:
        :return:
        """
        a = Asset(client)
        if assetModelId is not None:
            search_list = client.list_assets(assetModelId=assetModelId)["assetSummaries"]
        else:
            search_list = client.list_assets(filter="TOP_LEVEL")["assetSummaries"]
        for e in search_list:
            if e["name"] == assetName:
                a.assetId = e["id"]
                a.fetch(client=client)
                return a

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, m):
        raise NotImplementedError("It is not possible to set the model.")

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, m):
        raise NotImplementedError("It is not possible to set the attributes.")

    def fetch(self, deep=False, client=None):
        """
        fetches and updates attributes using the sitewise api
        :param client:
        :return: success status boolean
        """
        client = client or self._client
        assert self.assetId
        asset = client.describe_asset(assetId=self.assetId)
        for k, v in asset.items():
            if hasattr(self, k):
                setattr(self, k, v)

        if deep:
            # extract attributes
            from .Model import Model
            self._model = Model(assetModelId=self.assetModelId)
            self._model.fetch()
            self._attributes = []
            for ap in self.assetProperties:
                aa = AssetAttribute(assetId=self.assetId, propertyId=ap["id"])
                aa.fetch()
                self._attributes.append(aa)
        return True

    def create(self, doWait=False, timeout=5, doFetch=False, client=None):
        """

        :param client:
        :return:
        """

        client = client or self._client
        required_keys = ["assetName", "assetModelId"]
        kwargs = {k: getattr(self, k) for k in required_keys}
        attemps = 30
        while True:
            try:
                resp = client.create_asset(**kwargs)
            except:
                time.sleep(0.2)
                attemps -= 1
            else:
                break
            if attemps == 0:
                # one last try to raise the original exception
                resp = client.create_asset(**kwargs)

        self.assetId = resp["assetId"]
        self.assetArn = resp["assetArn"]
        self.assetStatus = resp["assetStatus"]
        c = timeout
        while doWait:
            try:
                self.fetch()
            except client.exceptions.ConflictingOperationException:
                time.sleep(0.2)
                c -= 0.2
            if self.assetStatus["state"] == "CREATING" or self.assetStatus["state"] == "PROPAGATING" and c > 0:
                time.sleep(0.2)
                c -= 0.2
            else:
                break
        if doFetch:
            self.fetch()
        return True

    def delete(self, doWait=False, timeout=5, client=None):
        """

        :param client:
        :return:
        """
        client = client or self._client
        assert self.assetModelId
        response = client.delete_asset(
            assetId=self.assetId
        )
        while doWait:
            try:
                client.describe_asset(assetId=self.assetId)
            except client.exceptions.ResourceNotFoundException:
                return response
            else:
                if timeout <= 0:
                    return response
                time.sleep(0.2)
                timeout -= 0.2
        return response

    def update(self, client=None, **kwargs):
        """

        :param client:
        :return:
        """
        client = client or self._client
        assert self.assetId
        required_keys = ["assetName", "assetModelId"]
        kwargs = {k: kwargs.get(k, getattr(self, k)) for k in required_keys}
        return client.update_asset(**kwargs)
