from apscheduler.schedulers.background import BackgroundScheduler
from app.ocr.ocr_processor import document_process
import time


def start_scheduler(app):
    print("Starting scheduler...")

    scheduler = BackgroundScheduler()
    scheduler.add_job(document_process(app), 'interval', seconds=5, max_instances=3)

    with app.app_context():
        scheduler.start()
        app.logger.info("Scheduler started")

        try:
            while True:
                time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
            app.logger.info("Scheduler stopped")
