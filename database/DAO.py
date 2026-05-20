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

    @staticmethod
    def getPopolaritaArtisti(genere):
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """select ar.ArtistId, ar.Name, sum(il.Quantity ) as pop
                    from Artist ar, Album al, Track t, Genre g, InvoiceLine il
                    where ar.ArtistId = al.ArtistId 
                    and al.AlbumId = t.AlbumId 
                    and t.GenreId = g.GenreId 
                    and t.TrackId = il.TrackId 
                    and g.Name =%s
                    group by ar.ArtistId, ar.Name """
        cursor.execute(query, (genere,))

        for row in cursor:
            artista = Artist(ArtistId=row["ArtistId"], Name=row["Name"])
            result[artista] = row["pop"]

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getClientiArtista(artistId):
        conn = DBConnect.get_connection()

        result = set()

        cursor = conn.cursor(dictionary=True)
        query = """select distinct i.CustomerId 
                    from Invoice i, InvoiceLine il, Track t, Album al
                    where i.InvoiceId = il.InvoiceId 
                    and il.TrackId = t.TrackId 
                    and t.AlbumId = al.AlbumId 
                    and al.ArtistId = %s"""
        cursor.execute(query, (artistId,))

        for row in cursor:
            result.add(row["CustomerId"])

        cursor.close()
        conn.close()
        return result
