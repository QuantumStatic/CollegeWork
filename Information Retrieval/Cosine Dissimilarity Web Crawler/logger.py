import logging
import os

class simpleWebCrawlerLogger:
    def __init__(self, name:str, filename:str, level:int=logging.INFO, logging_format:str = "%(message)s"):
        self.logger_name = name
        self.filename = F"logs/{filename}"
        self.level = level
        self.format = logging_format

        os.makedirs('logs', exist_ok=True)
        with open(self.filename, 'w'):
            pass

        # Create a logger with the given name
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(self.level)

        # Create a file handler for outputting to a file
        file_handler = logging.FileHandler(self.filename)
        file_handler.setLevel(self.level)

        # Create a formatter and add it to the handlers
        formatter = logging.Formatter(self.format)
        file_handler.setFormatter(formatter)

        # Add the handlers to the logger
        self.logger.addHandler(file_handler)


    def log_link_info(self, log_string:str):
        self.logger.info(log_string)
    
    def log_empty_line(self):
        self.logger.info("-" * 265)

    def log_lang_info(self, lang_info:dict[str, int]):
        for lang_name, count in lang_info.items():
            self.logger.info(f"{lang_name}: {count}")