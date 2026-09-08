import os
import sys
import logging

from logging.handlers import TimedRotatingFileHandler
from pathlib import Path






BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_DIR = BASE_DIR / "logs"


LOG_DIR.mkdir(parents=True, exist_ok=True)



FILE_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s"
CONSOLE_FORMAT = "%(asctime)s | %(levelname)-8s | %(message)s"







class ColoredFormatter(logging.Formatter):
    """
    继承自 logging.Formatter，目的是重写 format 方法
    让控制台输出带有颜色，方便调试
    下面这些奇怪的字符串是 "ANSI 转义码"，终端看到这些代码就会变色
    """
    grey = "\x1b[38;20m"        
    green = "\x1b[32;20m"       
    yellow = "\x1b[33;20m"      
    red = "\x1b[31;20m"         
    bold_red = "\x1b[31;1m"     
    reset = "\x1b[0m"           
    format_str = CONSOLE_FORMAT 

    FORMATS = {
        logging.DEBUG: grey + format_str + reset,       
        logging.INFO: green + format_str + reset,       
        logging.WARNING: yellow + format_str + reset,   
        logging.ERROR: red + format_str + reset,        
        logging.CRITICAL: bold_red + format_str + reset
    }
    
    def format(self, record):
        
        log_fmt = self.FORMATS.get(record.levelno)
        
        formatter = logging.Formatter(log_fmt, datefmt="%H:%M:%S")
        
        return formatter.format(record)




def get_logger(name="tools_multi_agent"):
    """
    获取配置好的 Logger 实例
    """
    logger = logging.getLogger(name)

    
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)  

    
    console_handler = logging.StreamHandler(sys.stdout)         
    console_handler.setLevel(logging.INFO)  
    console_handler.setFormatter(ColoredFormatter())
    logger.addHandler(console_handler)

    
    
    app_handler = TimedRotatingFileHandler(
        filename=LOG_DIR / "app.log",
        when="midnight",  
        interval=1,       
        backupCount=30,   
        encoding="utf-8"  
    )
    app_handler.setLevel(logging.INFO)      
    app_handler.setFormatter(logging.Formatter(FILE_FORMAT))  
    logger.addHandler(app_handler)

    
    
    error_handler = TimedRotatingFileHandler(
        filename=LOG_DIR / "error.log",
        when="midnight",
        interval=1,
        backupCount=60, 
        encoding="utf-8"
    )
    error_handler.setLevel(logging.ERROR)       
    error_handler.setFormatter(logging.Formatter(FILE_FORMAT))
    logger.addHandler(error_handler)

    
    
    agent_handler = TimedRotatingFileHandler(
        filename=LOG_DIR / "agent_debug.log",
        when="midnight",
        interval=1,
        backupCount=7,  
        encoding="utf-8"
    )
    agent_handler.setLevel(logging.DEBUG)
    agent_handler.setFormatter(logging.Formatter(FILE_FORMAT))
    logger.addHandler(agent_handler)

    return logger



logger = get_logger()
