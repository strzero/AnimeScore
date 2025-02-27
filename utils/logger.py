import logging
import os
import time

from data.config import log_level
from data.config import work_dir


def return_level():
    if log_level == "INFO":
        return logging.INFO
    elif log_level == "DEBUG":
        return logging.DEBUG
    else:
        return logging.INFO


class Log:
    def __init__(self, logger=None):
        self.log_path = os.path.join(work_dir, "data", "log.txt")

        self.logger = logging.getLogger(logger)
        self.logger.setLevel(return_level())
        self.log_time = time.strftime("%Y_%m_%d")
        # 创建日志文件
        try:
            f = open(self.log_path, "x")
        except:
            f = open(self.log_path, "w")

        self.logger = logging.getLogger(logger)
        self.logger.setLevel(return_level())

        self.fh = logging.FileHandler(self.log_path, "a", encoding="utf-8")
        self.fh.setLevel(return_level())

        self.ch = logging.StreamHandler()
        self.ch.setLevel(return_level())

        formatter = logging.Formatter(
            "[%(asctime)s][%(filename)s][%(funcName)s][line:%(lineno)d][%(levelname)s] - %(message)s"
        )
        self.fh.setFormatter(formatter)
        self.ch.setFormatter(formatter)

        self.logger.addHandler(self.fh)
        self.logger.addHandler(self.ch)

        self.ch.close()
        self.fh.close()

    def getlog(self):
        return self.logger
