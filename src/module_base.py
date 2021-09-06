import logging

class ModuleBase(object):

    def __init__(self, module_name):
        self.__module_logger = logging.getLogger(module_name)
        self.__module_logger.setLevel(logging.DEBUG)

        self.registerLoggerHandler(logging.DEBUG)

    def registerLoggerHandler(self, level):
        handler = logging.StreamHandler()
        handler.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(name)-13s - %(levelname)-8s - %(message)s')
        handler.setFormatter(formatter)

        if len(self.__module_logger.handlers) > 0:
            for handler in self.__module_logger.handlers:
                if not isinstance(handler, logging.StreamHandler):
                    self.__module_logger.addHandler(handler)
        else:    
            self.__module_logger.addHandler(handler)

    def unregisterLoggerHandlers(self):
        # iterate over a copy of the handlers list
        for handler in self.__module_logger.handlers[:]:
             self.__module_logger.removeHandler(handler)

        self.__module_logger = None

    def moduleLogDebug(self, msg):
        self.__module_logger.log( logging.DEBUG, msg )

    def moduleLogInfo(self, msg):
        self.__module_logger.log( logging.INFO, msg )

    def moduleLogWarning(self, msg):
        self.__module_logger.log( logging.WARNING, msg )

    def moduleLogError(self, msg):
        self.__module_logger.log( logging.ERROR, msg )

    def moduleLogCritical(self, msg):
        self.__module_logger.log( logging.CRITICAL, msg )

    
