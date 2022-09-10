import os
from rich.traceback import install
from core.log import Logger
from core.algo import DET_curve
from core.swipe_extractor import write_all_word_logs
from core.user import process_files

from core.util import flatten, loadall

if __name__ == "__main__":
    install()
    log = Logger()
    log.km_info("Generating word log files...")
    write_all_word_logs()
    log.km_info("Generating Impostor and Genuine Score Files...")
    log.km_info("Generating Impostor and Genuine Score Files...")