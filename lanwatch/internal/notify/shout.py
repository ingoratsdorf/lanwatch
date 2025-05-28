import logging
from shoutrrr import Shoutrrr

def shout(message: str, url: str) -> None:
    """
    Send message with shoutrrr
    
    Args:
        message: The message to send
        url: The shoutrrr URL for notification service
    """
    if url:
        try:
            Shoutrrr(url).send(message)
        except Exception as e:
            logging.error(f"Notification failed (shoutrrr): {e}")
