# SitewisePyObjects

Map Sitewise Models and Assets to Python objects with CRUD operations




# Getting Started


`git clone https://github.com/paszin/SitewisePyObjects`

`pip install SitewisePyObjects`

or 


`pip install git+https://github.com/paszin/SitewisePyObjects`


# Usage


## Model

```python
from SitewisePyObjects.Model import Model
```

```python
# create a new model
m = Model(assetModelName="My Dummy Model", assetModelDescription="Created with SitewisePyObjects")
m.create()
```

```python
# print model & view properties
print(m)
for k, v in m:
    print(k, ":", v)
```

```
<Model: My Dummy Model - 37d022c2-ab15-47c6-9add-662f7d800367>
assetModelId : 37d022c2-ab15-47c6-9add-662f7d800367
assetModelArn : arn:aws:iotsitewise:eu-central-1:307341958296:asset-model/37d022c2-ab15-47c6-9add-662f7d800367
assetModelName : Pascals Dummy Model Updated
assetModelDescription : Created with SitewisePyObjects
assetModelProperties : []
assetModelHierarchies : []
assetModelCompositeModels : []
```

```python
# Update
m.assetModelName = "My Dummy Model Updated"
m.update()
```

```python
# Delete
m.delete()
```

```python
# Get existing Model by name
m = Model.fetch_by_name("A Model")

```

```python
# get all models with name "*Dummy*" and list their assets
from SitewisePyObjects.Model import Model
from SitewisePyObjects.Asset import Asset
import boto3
client = boto3.client("iotsitewise")

filter_function = lambda name: "Dummy" in name

for mi in client.list_asset_models()["assetModelSummaries"]:
    if filter_function(mi["name"]):
        m = Model.fetch_by_name(mi["name"])
        print(m)
        for a in m.get_assets():
            print("\t", a)

```

```
<Model: Pascals Dummy Model - 2803d879-d652-41e3-a89c-0d2481de800e>
	 <Asset: Pascals Dummy Asset 1>
     <Asset: Pascals Dummy Asset 2>
<Model: Pascals Dummy Model Updated - 36f7c25d-48ce-4139-8c2d-8dd7b9ce68fb>
	 <Asset: Pascals Dummy Asset>

```

# Features

(only checked features are supported!)

- [x] CRUD Operations for Models
- [x] find Model by name
- [ ] find Model by name out of 50+ models
- [x] CRUD Operations for Asset
- [x] find Asset by name and given model id
- [x] get assets from Model
- [ ] support for 50+ assets 
- [ ] CRUD operations for tags
- [ ] Update properties of Asset
- [ ] Update measurements of Asset
- [x] delete all Asset of a Model --> a.delete() for a in model.get_assets()
- [ ] handle hierarchies
- [x] add attribute to a Model
- [x] wait for Asset deletions
- [x] wait for Model deletions
- [x] wait for Model creation
- [ ] handle timestamps in AssetAttributes