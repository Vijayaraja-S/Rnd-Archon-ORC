import base64
import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO
from typing import List

import cv2
import numpy as np
from PIL import Image

from .ocr_process import OCRProcess
from .paddleocrprocess import PaddleOcrProcess
from ..enums.document_status import DocumentStatus
from ..extensions import db
from ..model import Document
from ..model.beans import request_bean
from ..service import FieldsService
from ..service.document_service import DocumentService


def fix_base64_padding(base64_string):
    padding_needed = 4 - (len(base64_string) % 4)
    if padding_needed:
        base64_string += "=" * padding_needed
    return base64_string


def process_ocr(document: Document, field_details_list, ocr_processor: OCRProcess):
    image_data = document.image_content
    image_data = fix_base64_padding(image_data)
    image_data = base64.b64decode(image_data)
    image_pil = Image.open(BytesIO(image_data))
    image_pil = image_pil.convert('RGB')
    image_np = np.array(image_pil)
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    doc_id = document.id
    ocr_processor.fetch_values_from_ocr(image_cv, field_details_list, doc_id)


def choose_ocr_processor(ocr_type: str) -> OCRProcess:
    ocr_processors = {
        "paddle": PaddleOcrProcess(),
    }
    return ocr_processors.get(ocr_type.lower(), None)


def init_ocr(document: Document, ocr_type: str):
    try:
        list_of_fields = FieldsService.get_fields_by_doc_type(document.document_type_id)
        field_details_list: List[request_bean.FieldDetailsBuilder] = []

        for field in list_of_fields:
            binding_name = field.binding_name
            coordinates = field.coordinates
            if isinstance(coordinates, str):
                coordinates = json.loads(coordinates)
            position = request_bean.Position(**coordinates)
            field_details = request_bean.FieldDetailsBuilder(id=field.id, binding_name=binding_name, position=position)
            field_details_list.append(field_details)

        ocr_processor = choose_ocr_processor(ocr_type)
        if ocr_processor:
            process_ocr(document, field_details_list, ocr_processor)
        else:
            logging.error(f"Invalid OCR type: {ocr_type}")

    except Exception as e:
        logging.error(f"Error processing document {document.id}: {e}")
        raise


def process_single_document(doc, app):
    try:
        with app.app_context():
            init_ocr(doc, "paddle")
            document = Document.query.filter_by(id=doc.id).first()
            if document:
                document.status = DocumentStatus.PROCESSED
                db.session.add(document)
                db.session.commit()
            logging.info("Document {doc.id} processed successfully")
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
            documents = DocumentService.get_doc_by_status(DocumentStatus.SCHEDULED)
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
