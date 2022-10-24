# eva-ls-ml
Label Studio ML backend, made using EVA Database

All the routes supported by eva-ls-backend (incoming requests)  
| route | call|
|:------|-----:|
|predict    | [_manager.predict()](https://github.com/heartexlabs/label-studio-ml-backend/blob/01829ba15221102f0f54ab4b1b07ce51d70fe3d7/label_studio_ml/model.py#L589)|
|setup      | [_manager.fetch()](https://github.com/heartexlabs/label-studio-ml-backend/blob/01829ba15221102f0f54ab4b1b07ce51d70fe3d7/label_studio_ml/model.py#L499)|
|train      | [_manager.train()](https://github.com/heartexlabs/label-studio-ml-backend/blob/01829ba15221102f0f54ab4b1b07ce51d70fe3d7/label_studio_ml/model.py#L708)|
|webhook    | [_manager.webhook()](https://github.com/heartexlabs/label-studio-ml-backend/blob/01829ba15221102f0f54ab4b1b07ce51d70fe3d7/label_studio_ml/model.py#L734)|
|is_training| [_manager.is_training()](https://github.com/heartexlabs/label-studio-ml-backend/blob/01829ba15221102f0f54ab4b1b07ce51d70fe3d7/label_studio_ml/model.py#L557)|
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

Label Studio API [documentation](https://labelstud.io/api#tag/Machine-Learning)