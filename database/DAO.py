from database.DB_connect import DBConnect


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllGenre():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary = True)
        query = """select *
                   from genre g """
        cursor.execute(query)

        for row in cursor:
            result.append(row["Name"])

        cursor.close()
        conn.close()
        return result
