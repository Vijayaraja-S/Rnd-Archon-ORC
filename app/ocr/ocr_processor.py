import base64
import logging
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from typing import List

import cv2
import numpy as np
from PIL import Image
from paddleocr import PaddleOCR

from ..enums import document_status
from ..models import Document, Fields
from ..models.beans import request_bean
from ..services import FieldsService, DocumentFieldService
from ..services.document_service import DocumentService


def process_ocr(document: Document, field_details_list):
    image_data = base64.b64decode(document.image_content)

    image_pil = Image.open(BytesIO(image_data))
    image_pil = image_pil.convert('RGB')
    image_np = np.array(image_pil)
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    start_process(field_details_list, image_cv, document.document_id)


def init_ocr(document: Document):
    try:
        list_of_fields: List[Fields] = FieldsService.get_fields_by_doc_type(document.id)
        field_details_list: List[request_bean.FieldDetailsBuilder] = []

        for field in list_of_fields:
            binding_name = field.binding_name
            coordinates = field.coordinates

            position = request_bean.Position(**coordinates)
            field_details = request_bean.FieldDetailsBuilder(id=field.id, binding_name=binding_name, position=position)
            field_details_list.append(field_details)

        process_ocr(document, field_details_list)

    except Exception as e:
        # Log the exception with the document ID for context
        logging.error(f"Error processing document {document.id}: {e}")
        # Optionally, you might want to raise the exception or handle it accordingly
        raise


def document_process(app):
    print("Process OCR starting...")
    try:
        with app.app_context():  # Push the application context
            documents: List[Document] = DocumentService.get_doc_by_status(document_status.DocumentStatus.SCHEDULED)
            doc_counts = len(documents)

            if doc_counts > 0:
                with ThreadPoolExecutor(max_workers=doc_counts) as executor:
                    futures = []
                    for doc in documents:
                        try:
                            future = executor.submit(init_ocr, doc)
                            futures.append(future)
                        except Exception as e:
                            logging.error(f"Error submitting job for document {doc.id}: {e}")

                    for future in futures:
                        try:
                            future.result()
                        except Exception as e:
                            logging.error(f"Error occurred during processing: {e}")

    except Exception as e:
        logging.error(f"Error in document_process: {e}")


def start_process(beans, processed_image, document_id):
    return fetch_values_from_paddle_ocr(processed_image, beans, document_id)


def fetch_values_from_paddle_ocr(img, beans, doc_id):
    thresh = 255 - cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)
    result = retrieve_results(thresh, ocr)

    for res in result[0]:
        bbox = res[0]
        for bean in beans:
            if is_bounding_box_within(bbox, bean.position) and res[0] and res[1]:
                accuracy = res[1][1]
                if accuracy > 0.50:
                    value = res[1][0]
                    DocumentFieldService.save_field_document_info(bean.id, doc_id, value)


def retrieve_results(thresh, ocr):
    return ocr.ocr(thresh, cls=True)


def is_bounding_box_within(bounding_box, position: request_bean.Position):
    x1, y1 = bounding_box[0]
    x2, y2 = bounding_box[3]
    pos_x = position.x
    pos_y = position.y
    pos_width = position.width
    pos_height = position.height

    return x1 >= pos_x and y1 >= pos_y and x2 <= pos_x + pos_width and y2 <= pos_y + pos_height
