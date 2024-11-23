import logging
import os

def get_logger(name=__name__, log_level=logging.INFO, log_file=None):
    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Avoid duplicate handlers if logger is already set up
    if logger.hasHandlers():
        return logger

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (optional)
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)  # Create directory if it doesn't exist
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

logger = get_logger("click_helper")

def retry(times: int, exceptions: tuple[type(Exception)] = (Exception,)):
    """
    Retry decorator for functions that might fail.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    logger.debug(f"Attempt {attempt + 1} for {func.__name__}")
                    return func(*args, **kwargs)
                except exceptions as e:
                    logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}")
            logger.error(f"Max retries reached for {func.__name__}")
            raise exceptions[0]

        return wrapper

    return decorator
