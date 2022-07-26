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
    # write_all_word_logs()
    log.km_info("Generating Impostor and Genuine Score Files...")
    # process_files()
    log.km_info("Creating DET curve...")
    s = 0
    genuine_scores_list = flatten(
        list(loadall("/Users/alvinkuruvilla/Dev/swipe-type/aws-genuine.dat"))
    )
    impostor_scores_list = []
    p = os.path.join(os.getcwd(), "impostors_data")
    folder_names = [f for f in os.listdir(p) if os.path.isdir(os.path.join(p, f))]
    # print(folder_names)
    for folder_name in folder_names:
        p2 = os.path.join(os.getcwd(), "impostors_data", folder_name)
        file_names = [f for f in os.listdir(p2) if os.path.isfile(os.path.join(p2, f))]
        for file in file_names:
            # print(os.path.join(p2, file))
            s += len(flatten(list((loadall(os.path.join(p2, file))))))
            impostor_scores_list.append(
                (flatten(list((loadall(os.path.join(p2, file))))))
            )
    # print(flatten(impostor_scores_list))
    # print(len(flatten(impostor_scores_list)))
    # print("SUM:", s)
    DET_curve(0, 8000, genuine_scores_list, flatten(impostor_scores_list))
