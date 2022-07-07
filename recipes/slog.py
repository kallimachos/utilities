#!/bin/python3
"""Basic example using structlog."""

from logging import DEBUG, INFO

import structlog

# Log levels  -  https://docs.python.org/3/howto/logging.html#when-to-use-logging
# DEBUG    Detailed information, typically of interest only when diagnosing
#          problems.
# INFO 	   Confirmation that things are working as expected.
# WARNING  An indication that something unexpected happened, or indicative of
#          some problem in the near future (e.g. disk space low). The software
#          is still working as expected.
# ERROR    Due to a more serious problem, the software has not been able to
#          perform some function.
# CRITICAL A serious error, indicating that the program itself may be unable to
#          continue running.

logger = structlog.get_logger()


def logconfig(debug=False, console=False):
    """Set logging configuration.

    Args:
        debug (bool, optional): True to set loglevel to DEBUG
        console (bool, optional): True if logging to console.

    """
    call_processor = [
        structlog.processors.CallsiteParameterAdder(
            parameters={
                structlog.processors.CallsiteParameter.FILENAME: "filename",
                structlog.processors.CallsiteParameter.MODULE: "module",
                structlog.processors.CallsiteParameter.FUNC_NAME: "func_name",
                structlog.processors.CallsiteParameter.LINENO: "lineno",
            }
        ),
    ]
    if console:
        level_styles = structlog.dev.ConsoleRenderer.get_default_level_styles()
        del level_styles["debug"]
        processors = call_processor if debug else []
        processors.append(structlog.dev.ConsoleRenderer(level_styles=level_styles))
    else:
        processors = call_processor + [
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ]
    loglevel = DEBUG if debug else INFO
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(loglevel),
        processors=[structlog.processors.add_log_level] + processors,
    )
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    try:
        assert True is False
    except AssertionError:
        logger.exception("This is an exception message")
    return


if __name__ == "__main__":
    logconfig(True, True)
