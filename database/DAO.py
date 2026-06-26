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

    @staticmethod
    def getAllArtist(g):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct a.ArtistId , a.Name 
                    from artist a, album al, track t
                    where a.ArtistId = al.ArtistId and al.AlbumId = t.AlbumId
                    and t.GenreId = %s"""
        cursor.execute(query,(g,))

        for row in cursor:
            result.append(Artista(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(g):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select al1.ArtistId as a1 , al2.ArtistId as a2
                    from album al1, album al2,track t1 , track t2, invoiceline il1, invoiceline il2, invoice i1, invoice i2
                    where al1.AlbumId = t1.AlbumId and t1.TrackId = il1.TrackId and il1.InvoiceId = i1.InvoiceId 
                    and al2.AlbumId = t2.AlbumId and t2.TrackId = il2.TrackId and il2.InvoiceId = i2.InvoiceId 
                    and al1.ArtistId < al2.ArtistId 
                    and i1.CustomerId = i2.CustomerId
                    and t1.GenreId = %s and t2.GenreId = %s
                    group by al1.ArtistId , al2.ArtistId"""
        cursor.execute(query, (g,g))

        for row in cursor:
            result.append((row['a1'],row['a2']))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllPop():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct a.ArtistId as art, count(i.TrackId ) as pop
                    from album a, track t, invoiceline i 
                    where a.AlbumId = t.AlbumId and t.TrackId = i.TrackId 
                    group by art"""
        cursor.execute(query)

        for row in cursor:
            result.append((row['art'], row['pop']))
        cursor.close()
        conn.close()
        return result






