import logging
import os

class ModuleLogger:
    def __init__(self, module_name):
        self.logger = self._create_logger(module_name)

    @staticmethod
    def _create_logger(module_name):
        logger = logging.getLogger(module_name)
        log_path = os.path.join('./logs', f"{module_name}.log")

        if not os.path.exists('./logs'):
            os.makedirs('./logs')

        file_handler = logging.FileHandler(log_path)
        formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s]\n\t\t\t%(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.setLevel(os.environ.get("DEBUG_LEVEL", "INFO"))

        return logger

    def get_logger(self):
        return self.logger