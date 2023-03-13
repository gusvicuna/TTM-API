import mongoengine


def getDB():
    username = "gpvicuna"
    password = "Night1139"
    db_name = "test"
    client = mongoengine.connect(
        host=f"mongodb+srv://{username}:{password}@{db_name}" +
        ".0v1hxpd.mongodb.net/test")
    db = client["test"]

    return db
