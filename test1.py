import logging
path = "./"

error_logger = logging.getLogger("error")
error_logger.setLevel(logging.ERROR)
error_handler = logging.FileHandler(path+"log/error.log")
error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
error_logger.addHandler(error_handler)
info_logger = logging.getLogger("info")
info_logger.setLevel(logging.INFO)
info_handler = logging.FileHandler(path + "log/info.log")
info_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
info_logger.addHandler(info_handler)

error_logger.error("test")
info_logger.info("123223")