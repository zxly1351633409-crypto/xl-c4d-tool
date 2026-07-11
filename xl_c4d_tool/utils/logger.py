"""【工具模块：日志系统】统一日志记录，输出到文件和控制台"""
import logging
import os
from datetime import datetime


def setup_logger(addon_name="xl_c4d_tool"):
    """配置日志器：文件日志(DEBUG级别) + 控制台日志(INFO级别)"""
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
    try:
        os.makedirs(log_dir, exist_ok=True)
    except OSError:
        pass  # 只读环境下降级为控制台日志

    log_file = os.path.join(log_dir, f"{addon_name}_{datetime.now().strftime('%Y%m%d')}.log")

    logger = logging.getLogger(addon_name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        fh = logging.FileHandler(log_file, encoding='utf-8')
        fh.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger


logger = setup_logger()
