from enum import Enum


class DocumentStatus(Enum):
    SCHEDULED = 'SCHEDULED'
    IN_PROGRESS = 'IN_PROGRESS'
    PROCESSED = 'PROCESSED'
    REVIEW = 'REVIEW'
    SKIPPED = 'SKIPPED'
    ERROR = 'ERROR'
