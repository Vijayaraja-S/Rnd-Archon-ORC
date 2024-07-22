import base64
import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO
from typing import List

import cv2
import numpy as np
from PIL import Image
from paddleocr import PaddleOCR

from ..extensions import db
from ..enums.document_status import DocumentStatus
from ..model import Document, Fields
from ..model.beans import request_bean
from ..service import FieldsService
from ..service.document_field_service import DocumentFieldService
from ..service.document_service import DocumentService


def fix_base64_padding(base64_string):
    padding_needed = 4 - (len(base64_string) % 4)
    if padding_needed:
        base64_string += "=" * padding_needed
    return base64_string


def process_ocr(document: Document, field_details_list):
    image_data = document.image_content

    image_data = fix_base64_padding(image_data)

    image_data = base64.b64decode(image_data)

    image_pil = Image.open(BytesIO(image_data))
    image_pil = image_pil.convert('RGB')
    image_np = np.array(image_pil)
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    doc_id = document.id
    fetch_values_from_paddle_ocr(image_cv, field_details_list, doc_id)


def init_ocr(document: Document):
    try:
        list_of_fields: List[Fields] = FieldsService.get_fields_by_doc_type(document.document_type_id)
        field_details_list: List[request_bean.FieldDetailsBuilder] = []

        for field in list_of_fields:
            binding_name = field.binding_name
            coordinates = field.coordinates

            if isinstance(coordinates, str):
                coordinates = json.loads(coordinates)

            position = request_bean.Position(**coordinates)
            field_details = request_bean.FieldDetailsBuilder(id=field.id, binding_name=binding_name, position=position)
            field_details_list.append(field_details)

        process_ocr(document, field_details_list)

    except Exception as e:
        logging.error(f"Error processing document {document.id}: {e}")
        raise


def process_single_document(doc, app):
    try:
        with app.app_context():
            init_ocr(doc)
            document = Document.query.filter_by(id=doc.id).first()
            if document:
                document.status = DocumentStatus.PROCESSED
                db.session.add(document)
                db.session.commit()
            logging.info(f"Document {doc.id} processed successfully")
    except Exception as e:
        logging.error(f"Error processing document {doc.id}: {e}")
        with app.app_context():
            document = Document.query.filter_by(id=doc.id).first()
            if document:
                document.status = DocumentStatus.ERROR
                db.session.add(document)
                db.session.commit()


def document_process(app):
    print("Process OCR starting...")
    try:
        with app.app_context():
            documents: List[Document] = DocumentService.get_doc_by_status(DocumentStatus.SCHEDULED)
            doc_counts = len(documents)

            if doc_counts == 0:
                print("No documents to process.")
                return

            with ThreadPoolExecutor(max_workers=doc_counts) as executor:
                futures = [executor.submit(process_single_document, doc, app) for doc in documents]
                for future in as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        logging.error(f"Error in future result: {e}")

    except Exception as e:
        logging.error(f"Error in document_process: {e}")


def start_process(beans, processed_image, document_id):
    return fetch_values_from_paddle_ocr(processed_image, beans, document_id)


def fetch_values_from_paddle_ocr(img, beans, doc_id):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    thresh = 255 - cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

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
