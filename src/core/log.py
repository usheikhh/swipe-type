import sys
from functools import partialmethod
from loguru import logger


class Logger:
    """A wrapper around python's native logging module to allow for prettier and more expressive logging output"""

    def __init__(self) -> None:
        format = "<level>{level: <8}</level> | <level>{message}</level>"
        logger.remove()
        logger.add(sys.stderr, format=format)

    def km_info(self, msg: str) -> None:
        """
        Displays an information level message to the user
        Parameters
        ----------
        msg: str
            The message to display
        Returns
        ----------
        None
        """
        logger.info(msg)

    def km_warn(self, msg: str) -> None:
        """
        Displays a warning level message to the user
        Parameters
        ----------
        msg: str
            The message to display
        Returns
        ----------
        None
        """
        logger.warning(msg)

    def km_error(self, msg: str) -> None:
        """
        Displays an error level message to the user
        Parameters
        ----------
        msg: str
            The message to display
        Returns
        ----------
        None
        """
        logger.error(msg)

    def km_fatal(self, msg: str) -> None:
        """
        Displays a fatal level message to the user
        Parameters
        ----------
        msg: str
            The message to display
        Returns
        ----------
        None
        """
        logger.level("FATAL", no=33, color="<fg #FFA500>")
        logger.__class__.km_fatal = partialmethod(logger.__class__.log, "FATAL")
        logger.km_fatal(msg)
