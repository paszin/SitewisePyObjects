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

