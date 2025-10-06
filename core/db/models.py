
class DataBaseConfig:
    def __init__(self, user, password, database, host, port):
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.port = port
    
    
    def __post_init__(self):
        if not all([self.user, self.password, self.database]):
            raise ValueError("Не указаны обязательные параметры подключения к БД")
    
    
    def to_dict(self) -> dict:
        return {
            "user": self.user,
            "password": self.password,
            "database": self.database,
            "host": self.host,
            "port": self.port,
        }
    
    def __repr__(self):
        return (
            f"DatabaseConfig(host={self.host!r}, port={self.port}, "
            f"database={self.database!r}, user={self.user!r})"
        )