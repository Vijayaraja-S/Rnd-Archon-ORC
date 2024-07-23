from abc import ABC

import cv2
from paddleocr import PaddleOCR

from .ocr_process import OCRProcess
from ..service.document_field_service import DocumentFieldService
from ..model.beans import request_bean


class PaddleOcrProcess(OCRProcess, ABC):

    @classmethod
    def is_bounding_box_within(cls, bounding_box, position: request_bean.Position):
        x1, y1 = bounding_box[0]
        x2, y2 = bounding_box[3]
        pos_x = position.x
        pos_y = position.y
        pos_width = position.width
        pos_height = position.height

        return x1 >= pos_x and y1 >= pos_y and x2 <= pos_x + pos_width and y2 <= pos_y + pos_height

    @classmethod
    def fetch_values_from_paddle_ocr(cls, img, beans, doc_id):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        thresh = 255 - cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)
        result = ocr.ocr(thresh, cls=True)

        for res in result[0]:
            bbox = res[0]
            for bean in beans:
                if cls.is_bounding_box_within(bbox, bean.position) and res[0] and res[1]:
                    accuracy = res[1][1]
                    if accuracy > 0.50:
                        value = res[1][0]
                        DocumentFieldService.save_field_document_info(bean.id, doc_id, value)
