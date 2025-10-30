class StateReporterEventTgb:
    def __init__(self, name: str, typeObject: str):
        self.__name = name
        self.__typeObject = typeObject

    @property
    def name(self):
        return self.__name

    def eventTgbEndWithCode(self, dataContext):
        print(f"\033[34m[DEBUG] [{self.__typeObject}: {self.__name}]: {dataContext}\033[0m")

    def eventTgbData(self, nameData, dataContext):
        print(f"\033[34m[DEBUG] [{self.__typeObject}: {self.__name}]: {nameData} - {dataContext}\033[0m")


class StateReporterHandler(StateReporterEventTgb):
    def __init__(self, __name: str):
        super().__init__(__name, "Handler")



class StateReporterMiddleware(StateReporterEventTgb):
    
    def __init__(self, __name: str):
        super().__init__(__name, "Middleware")    

    def middlewareStart(self):
        print(f"\033[32m[DEBUG] [MiddleWare: {super().name}]: START\033[0m")

    def middlewareEnd(self):
        print(f"\033[32m[DEBUG] [MiddleWare: {super().name}]: END\033[0m")