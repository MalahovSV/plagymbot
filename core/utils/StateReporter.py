
class StateReporterMiddleware:
    
    def __init__(self, nameMiddleware: str):
        self.nameMiddleware = nameMiddleware

    def middlewareStart(self):
        print(f"\033[32m[DEBUG] [MiddleWare: {self.nameMiddleware}]: START\033[0m")

    def middlewareEnd(self):
        print(f"\033[32m[DEBUG] [MiddleWare: {self.nameMiddleware}]: END\033[0m")
    
    def middlewareEndWithCode(self, dataContext):
        print(f"\033[34m[DEBUG] [MiddleWare: {self.nameMiddleware}]: {dataContext}\033[0m")

    def middlewareData(self, nameData, dataContext):
        print(f"\033[34m[DEBUG] [MiddleWare: {self.nameMiddleware}]: {nameData} - {dataContext}\033[0m")