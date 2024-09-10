from threading import Thread
from bot import run_bot
from db_manager import clean_db
if __name__ == '__main__':
    Thread(target=clean_db).start()
    run_bot()