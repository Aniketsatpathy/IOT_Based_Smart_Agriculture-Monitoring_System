from logger import system_logger

def log_event(event: str):
    """
    Logs a system event in a standardized format so it can be parsed by the dashboard.
    """
    system_logger.info(f"EVENT: {event}")
