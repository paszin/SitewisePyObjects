import time

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

    @staticmethod
    def fetch_by_name(assetModelName, client=boto3.client("iotsitewise")):
        """
        :param assetModelName: Name of the model
        :param client:
        :return:
        """
        m = Model(client)
        for e in client.list_asset_models()["assetModelSummaries"]:
            if e["name"] == assetModelName:
                m.assetModelId = e["id"]
                m.fetch(client=client)
                return m



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


    def create(self, doWait=False, timeout=5, client=None):
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
        while doWait:
            self.fetch()
            if self.assetModelStatus["state"] == "CREATING" or self.assetModelStatus["state"] == "PROPAGATING" or timeout <= 0:
                time.sleep(0.2)
                timeout -= 0.2
            else:
                break
        return True


    def delete(self, doWait=False, timeout=5, client=None):
        """

        :param client:
        :return:
        """
        client = client or self._client
        assert self.assetModelId
        response = client.delete_asset_model(
            assetModelId=self.assetModelId
        )
        while doWait:
            try:
                client.describe_asset_model(assetModelId=self.assetModelId)
            except client.exceptions.ResourceNotFoundException:
                return response
            else:
                if timeout <= 0:
                    return response
                time.sleep(0.2)
                timeout -= 0.2
        return response

    def update(self, client=None):
        """

        :param client:
        :return:
        """
        client = client or self._client
        assert self.assetModelId
        required_keys = ["assetModelId", "assetModelName", "assetModelDescription", "assetModelProperties", "assetModelHierarchies", "assetModelCompositeModels"]
        kwargs = {k: getattr(self, k) for k in required_keys}
        return client.update_asset_model(**kwargs)

    def get_assets(self, fetch_assets=False, client=None):
        """
        :param fetch_assets: boolean, set to True to fetch all information regarding
        :param client:
        :return: list of Assets
        """
        client = client or self._client
        from .Asset import Asset
        assets = []
        for e in client.list_assets(assetModelId=self.assetModelId)["assetSummaries"]:
            a = Asset(assetId=e["id"], assetArn=e["arn"], assetName=e["name"], assetModelId=e["assetModelId"], assetCreationDate=e["creationDate"], assetLastUpdateDate=e["lastUpdateDate"], assetStatus=e["status"])
            if fetch_assets:
                a.fetch()
            assets.append(a)
        return assets

    def add_attribute(self, name, dataType, defaultValue=None, doUpdate=True):

        inner_part = {"defaultValue": defaultValue}
        if defaultValue is None:
            inner_part = {}
        new_att = {
            "name": name,
            "dataType": dataType,
            "type": {
                "attribute": inner_part
            }
        }

        self.assetModelProperties.append(new_att)

        if doUpdate:
            self.update()
        return True

    def add_measurement(self, name, unit, dataType, doUpdate=True):

        new_att = {
            "name": name,
            "dataType": dataType,
            "unit": unit,
            "type": {"measurement": {}}}
        self.assetModelProperties.append(new_att)

        if doUpdate:
            self.update()
        return True




