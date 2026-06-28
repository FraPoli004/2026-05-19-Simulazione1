from database.DB_connect import DBConnect
from model.genre import Genre
from model.artista import Artista


class DAO():
    @staticmethod
    def getAllGenres():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM genre"
        cursor.execute(query)

        for row in cursor:
            result.append(Genre(**row))
        cursor.close()
        conn.close()
        return result







