from enum import Enum


class DocumentStatus(Enum):
    SCHEDULED = 'SCHEDULED'
    IN_PROGRESS = 'IN_PROGRESS'
    PROCESSED = 'Processed'
    REVIEW = 'Review'
    SKIPPED = 'Skipped'
    ERROR = 'Error'
