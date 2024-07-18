from enum import Enum

class DocumentStatus(Enum):
    REVIEW = 'Review'
    PROCESSED = 'Processed'
    ERROR = 'Error'
    SKIPPED = 'Skipped'