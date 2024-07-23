import threading

from apscheduler.schedulers.background import BackgroundScheduler
from app.ocr.processor import document_process


def start_scheduler(app):
    print("Starting scheduler...")

    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: document_process(app), 'interval', seconds=5, max_instances=1)

    def run_scheduler():
        with app.app_context():
            scheduler.start()
            app.logger.info("Scheduler started")
            
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
