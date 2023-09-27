class Logger:
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4

    def __init__(self, level=DEBUG):
        self.level = level

    def debug(self, message):
        if self.level <= self.DEBUG:
            self._print_log("DEBUG", message)

    def info(self, message):
        if self.level <= self.INFO:
            self._print_log("INFO", message)

    def warning(self, message):
        if self.level <= self.WARNING:
            self._print_log("WARNING", message)

    def error(self, message):
        if self.level <= self.ERROR:
            self._print_log("ERROR", message)

    def _print_log(self, level_name, message):
        print("[{}] {}".format(level_name, message))

def main():
    # Usage:
    logger = Logger(Logger.INFO)
    my_str = "hello"
    my_num = 123

    logger.debug("This is a debug message.")  # Won't be printed
    logger.info(f"my_str={my_str}, my_num={my_num}")   # Will be printed
    logger.warning(f"my_str={my_str}, my_num={my_num}")  # Will be printed
    logger.error(f"my_str={my_str}, my_num={my_num}")   # Will be printed

if __name__ == "__main__":
    main()
