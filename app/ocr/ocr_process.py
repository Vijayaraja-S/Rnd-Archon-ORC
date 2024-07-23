from abc import ABC, abstractmethod


class OCRProcess(ABC):
    @abstractmethod
    def fetch_values_from_ocr(self, image, beans, doc_id):
        pass
