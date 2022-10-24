import logging
import pandas as pd
import os
import subprocess
import time
import boto3
from botocore.exceptions import ClientError

from eva.server.db_api import connect
from label_studio_ml.model import LabelStudioMLBase
from label_studio_ml.utils import DATA_UNDEFINED_NAME
from label_studio_tools.core.utils.io import get_data_dir

import nest_asyncio
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class EVADBModel(LabelStudioMLBase):

    def __init__(self, image_dir=None, score_threshold=0.3, device='cuda', **kwargs):

        subprocess.run(['eva_server'])
        time.sleep(10)

        nest_asyncio.apply()
        connection = connect(host='127.0.0.1', port=5432)
        self.cursor = connection.cursor()

        self.from_name, info = list(self.parsed_label_config.items())[0]
        self.to_name = info['to_name'][0]

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

    def predict(self, tasks, *kwargs):
        # assert len(tasks) == 1 (used in LS ML code)
        task = tasks[0]
        image_url = self._get_image_url(task)
        image_path = self.get_local_path(image_url)
        # TODO EVA result Pandas should be converted to the correct format
        self.cursor.execute('SELECT id, data, from myvideo')
        response = self.cursor.fetch_all()
        model_results = response.batch.frames
        # model_results = inference_detector(self.model, image_path)
        results = []
        all_scores = []
        img_width, img_height = get_image_size(image_path)
        for bboxes, label in zip(model_results, self.model.CLASSES):
            output_label = self.label_map.get(label, label)

            if output_label not in self.labels_in_config:
                print(output_label + ' label not found in project config.')
                continue
            for bbox in bboxes:
                bbox = list(bbox)
                if not bbox:
                    continue
                score = float(bbox[-1])
                if score < self.score_thresh:
                    continue
                x, y, xmax, ymax = bbox[:4]
                results.append({
                    'from_name': self.from_name,
                    'to_name': self.to_name,
                    'type': 'rectanglelabels',
                    'value': {
                        'rectanglelabels': [output_label],
                        'x': x / img_width * 100,
                        'y': y / img_height * 100,
                        'width': (xmax - x) / img_width * 100,
                        'height': (ymax - y) / img_height * 100
                    },
                    'score': score
                })
                all_scores.append(score)
        avg_score = sum(all_scores) / max(len(all_scores), 1)
        return [{
            'result': results,
            'score': avg_score
        }]
