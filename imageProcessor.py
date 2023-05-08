import psycopg2
from utilities import *

class imageProcessor:
    def __init__(self):
        self.conn = psycopg2.connect(database = "postgres", user = "postgres",
                         host = "192.168.204.7", password="reverseWikipedia",  connect_timeout=5
                        )
        self.cursor = self.conn.cursor()
        print("Connection Successful to PostgreSQL")
        """ self.cursor.execute(f"select * from hashes where %s = any(urls::text[])", ("https://en.wikipedia.org/wiki/Woodpigeon_(band)",))
        print(self.cursor.fetchone()) """
    def processImage(self, imageBinary, url):
        try:
            hashInt = getHashInt(imageBinary, False) #False, it has not been converted to an svg
            self.cursor.execute(f"INSERT INTO hashes(hash, url) VALUES ({hashInt}, %s)", (url,))
            self.conn.commit()
        except Exception as e:
            """
                This is most likely because there is an SVG that could not be parsed
            """
            print(url)
            print("either the image could not be read or the hash could not be added to the database")
            print(e)