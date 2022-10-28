import logging
import pandas as pd
import os
import subprocess
import time
import io
import json
import boto3
from botocore.exceptions import ClientError

from eva.server.db_api import connect
from label_studio_ml.model import LabelStudioMLBase
from label_studio_ml.utils import DATA_UNDEFINED_NAME
from label_studio_tools.core.utils.io import get_data_dir

import nest_asyncio
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


def json_load(file, int_keys=False):
    with io.open(file, encoding='utf8') as f:
        data = json.load(f)
        if int_keys:
            return {int(k): v for k, v in data.items()}
        else:
            return data

nest_asyncio.apply()
connection = connect(host='127.0.0.1', port=5432)
cursor =  connection.cursor()


class EVADBModel(LabelStudioMLBase):
    # TODO add script to make sure that eva_server starts
    # TODO add script to download java for eva

    def __init__(self, image_dir=None, labels_file=None, score_threshold=0.3, device='cuda', **kwargs):

        super(EVADBModel, self).__init__(**kwargs)
        print("parsed_label_config", self.parsed_label_config)
        # print('The variables is kwargs:', kwargs)
        

        self.labels_file = labels_file
        upload_dir = os.path.join(get_data_dir(), 'media', 'upload')
        self.image_dir = image_dir or upload_dir
        logger.debug(f'{self.__class__.__name__} reads images from {self.image_dir}')

        if self.labels_file and os.path.exists(self.labels_file):
            self.label_map = json_load(self.labels_file)
        else:
            self.label_map = {}

        self.from_name, info = list(self.parsed_label_config.items())[0]
        self.to_name = info['to_name'][0]
        self.value = info['inputs'][0]['value']

        schema = list(self.parsed_label_config.values())[0]

        self.labels_attrs = schema.get('labels_attrs')
        if self.labels_attrs:
            for label_name, label_attrs in self.labels_attrs.items():
                for predicted_value in label_attrs.get('predicted_values', '').split(','):
                    self.label_map[predicted_value] = label_name


    def _get_image_url(self, task):
        image_url = task['data'].get(self.value) or task['data'].get(DATA_UNDEFINED_NAME)
        if image_url.startswith('s3://'):
            # presign s3 url
            r = urlparse(image_url, allow_fragments=False)
            bucket_name = r.netloc
            key = r.path.lstrip('/')
            client = boto3.client('s3')
            try:
                image_url = client.generate_presigned_url(
                    ClientMethod='get_object',
                    Params={'Bucket': bucket_name, 'Key': key}
                )
            except ClientError as exc:
                logger.warning(f'Can\'t generate presigned URL for {image_url}. Reason: {exc}')
        return image_url
    
    def eva_to_ls_format(self, return_value):
        df = return_value.batch.frames
        
        return None
    
    def connect_to_eva(self):
        # cannot be started from here because the readout time is 3 seconds
        # subprocess.run(['eva_server'])
        # time.sleep(10)
        # nest_asyncio.apply()
        self.cursor = cursor

    def eva_query_result(self, video_path):
        self.cursor.execute('drop table myvideo')
        output_value = self.cursor.fetch_all()
        print(output_value)
        self.cursor.execute(f'load file "{video_path}" into myvideo')
        output_value = self.cursor.fetch_all()
        print(output_value)
        self.cursor.execute("""SELECT id, FastRCNNObjectDetector(data) 
                  FROM myvideo 
                  WHERE id < 20""")
        output_value = self.cursor.fetch_all()
        print(output_value)
        return self.eva_to_ls_format(output_value)

    def predict(self, tasks, **kwargs):
        # assert len(tasks) == 1 (used in LS ML code)
        print(tasks)
        task = tasks[0]
        video_url = self._get_image_url(task)
        video_path = self.get_local_path(video_url)
        print("\n\nPath for image is", video_path, "\n\n")
        # TODO EVA result Pandas should be converted to the correct format
        self.connect_to_eva()
        model_results = self.eva_query_result(video_path)
        print(model_results)

        predictions = []
        output = {
            'predictions': [

            ]
        }
        predictions = output
        
        return predictions

        

