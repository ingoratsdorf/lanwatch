import logging


class Data:
    def __init__(self):
        self.Use = ""
        self.Path = ""
        self.SQLitePath = ""
        self.PGConnect = ""
        self.PrimaryKey = ""


currentDB = Data()


def set_current_db():
    """Set the current database configuration based on the provided settings."""
    global currentDB

    if currentDB.Use == "postgres" and currentDB.PGConnect != "":
        currentDB.Path = currentDB.PGConnect
        currentDB.PrimaryKey = "BIGSERIAL PRIMARY KEY"
    else:
        currentDB.Use = "sqlite"
        currentDB.Path = currentDB.SQLitePath
        currentDB.PrimaryKey = "INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE"

    logging.info("Using DB: %s", currentDB.Use)


def set_current(config):
    """Set the current database configuration based on the provided config."""
    global currentDB
    currentDB.Use = config.UseDB
    currentDB.SQLitePath = config.DBPath
    currentDB.PGConnect = config.PGConnect

    set_current_db()
