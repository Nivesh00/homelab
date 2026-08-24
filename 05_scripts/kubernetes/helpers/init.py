import logging, argparse

from typing import Any

def setupCustomLogger(level: str = 'INFO') -> None:
    """
    Setup a custom logger which will be named 'main'
    :params level: level of the logger, not case sensitive
    """
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    handler: logging.StreamHandler = logging.StreamHandler()
    handler.setFormatter(formatter)

    level = level.lower()
    if level == "error":
        log_level = logging.ERROR
    elif level == "warn":
        log_level = logging.WARN
    elif level == "debug":
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logger: logging.Logger = logging.getLogger('main')
    logger.setLevel(log_level)
    logger.addHandler(handler)

    logging.getLogger('main').debug('Finished creating logger')

    return

def parseFlags() -> dict[str, Any]:
    """
    Parse flags set for the script
    :returns: A dictionary of flags and their values
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--log-level", help="Log level, one of [debug, info, warn, error]")
    parser.add_argument('-d', "--load-env", action='store_true', help="Set to load .env file")
    parser.add_argument('-c', "--incluster", action='store_true', help="Set if script is ran incluster")
    parser.add_argument('-k', "--kubeconfig", help="Path to kubeconfig file")
    args = parser.parse_args()

    flags_dict: dict[str, Any] = {
        'log-level': '' if args.log_level == None else args.log_level,
        'load-env': bool(args.load_env),
        'incluster': bool(args.incluster),
        'kubeconfig': '' if args.kubeconfig == None else args.kubeconfig
    }

    return flags_dict