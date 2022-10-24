# eva-ls-ml
Label Studio ML backend, made using EVA Database

All the routes supported by eva-ls-backend (incoming requests)  
| route | call|
|:------|-----:|
|predict    | _manager.predict()|
|setup      | _manager.fetch()|
|train      | _manager.train()|
|webhook    | _manager.webhook()|
|is_training| _manager.is_training()|
|health     | returns information about server|
|metrics    | returns nothing|
|versions   | returns version|

API routes called by the Label Studio server to eva-ls-backend from [Label Studio API routes file](https://github.com/heartexlabs/label-studio/blob/develop/label_studio/core/all_urls.json) (label studio requests)
```json
  {
    "url": "/api/ml/",
    "module": "ml.api.MLBackendListAPI",
    "name": "ml:api:ml-list",
    "decorators": ""
  },
  {
    "url": "/api/ml/<int:pk>",
    "module": "ml.api.MLBackendDetailAPI",
    "name": "ml:api:ml-detail",
    "decorators": ""
  },
  {
    "url": "/api/ml/<int:pk>/train",
    "module": "ml.api.MLBackendTrainAPI",
    "name": "ml:api:ml-train",
    "decorators": ""
  },
  {
    "url": "/api/ml/<int:pk>/interactive-annotating",
    "module": "ml.api.MLBackendInteractiveAnnotating",
    "name": "ml:api:ml-interactive-annotating",
    "decorators": ""
  },
  {
    "url": "/api/ml/<int:pk>/versions",
    "module": "ml.api.MLBackendVersionsAPI",
    "name": "ml:api:ml-versions",
    "decorators": ""
  },
```