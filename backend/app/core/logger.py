"""
日志配置
"""
import logging
import sys
from app.core.config import settings


def setup_logger():
    """配置日志"""
    logger = logging.getLogger("ddl-converter")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))

    # 控制台输出
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, settings.LOG_LEVEL))

    # 格式化
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


logger = setup_logger()
