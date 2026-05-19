from database.DB_connect import DBConnect
from model.artist import Artist


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

    @staticmethod
    def getAllArtists(genere):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct ar.ArtistId, ar.Name 
                    from artist ar, album al, track t, genre g 
                    where ar.ArtistId = al.ArtistId 
                    and al.AlbumId = t.AlbumId 
                    and t.GenreId = g.GenreId
                    and g.Name = %s"""
        cursor.execute(query, (genere,))

        for row in cursor:
            result.append(Artist(ArtistId=row["ArtistId"],
                                 Name=row["Name"]))

        cursor.close()
        conn.close()
        return result
