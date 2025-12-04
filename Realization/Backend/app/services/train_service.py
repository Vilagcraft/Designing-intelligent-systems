import subprocess
import threading
import time

from Realization.Backend.app.config import TRAIN_ENTRY, LOGS_DIR

TRAIN_STATUS = {
    "running": False,
    "last_run": None,
    "result": None,
    "pid": None
}

def _run_training(use_spark: bool):
    try:
        cmd = []

        if use_spark:
            cmd = ["spark-submit", str(TRAIN_ENTRY)]
        else:
            cmd = ["python3", str(TRAIN_ENTRY)]

        logfile = LOGS_DIR / f"train_{int(time.time())}.log"

        with open(logfile, "w") as f:
            p = subprocess.Popen(cmd, stdout=f, stderr=f)
            TRAIN_STATUS["pid"] = p.pid
            p.wait()

        TRAIN_STATUS["running"] = False
        TRAIN_STATUS["result"] = "success"
        TRAIN_STATUS["last_run"] = time.ctime()
    except Exception as e:
        TRAIN_STATUS["result"] = f"error: {e}"
        TRAIN_STATUS["running"] = False

def start_training(force: bool = False, use_spark: bool = False):
    if TRAIN_STATUS["running"]:
        return {"status": "Already running"}

    TRAIN_STATUS["running"] = True
    TRAIN_STATUS["result"] = None
    t = threading.Thread(target=_run_training, args=(use_spark,), daemon=True)
    t.start()

    return {"status": "training started"}

def get_train_status():
    return TRAIN_STATUS