import imagehash
from PIL import Image
import psycopg2
from utilities import *
import time
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
            #t1 = time.perf_counter()
            #self.cursor.execute(f"INSERT INTO hashes(hash, urls) VALUES ({hashInt}, ARRAY [ %s]) ON CONFLICT (hash) DO UPDATE SET urls = anyarray_concat_uniq(hashes.urls, ARRAY[%s])", (url, url,))
            #self.cursor.execute(f"INSERT INTO hashes(hash, urls) VALUES ({hashInt}, ARRAY [ %s]) ON CONFLICT (hash) DO UPDATE SET urls = array_append(hashes.urls, %s)", (url, url,))
            self.cursor.execute(f"INSERT INTO hashes(hash, url) VALUES ({hashInt}, %s)", (url,))
            self.conn.commit()
            #t2 = time.perf_counter()
            #print(t2-t1)
            """ self.cursor.execute(f"SELECT * FROM hashes WHERE hash <@ ({hashInt}, 0) limit 1")
            collumn = self.cursor.fetchone()
            if not collumn:
                # if row with this hash does not exist
                self.cursor.execute(f"INSERT INTO hashes(hash, urls) VALUES ({hashInt}, ARRAY [ %s])", (url,))
                self.conn.commit()
            else:
                self.cursor.execute(f"select * from hashes where id={collumn[0]} AND %s = any(urls::text[]) limit 1", (url,))
                if self.cursor.fetchone() is None:
                    self.cursor.execute(f"UPDATE hashes SET urls = array_append(urls, %s) WHERE id={collumn[0]}", (url,))
                    self.conn.commit() """
            #print(url + ": " + str(hashInt))
        except Exception as e:
            """
                This is most likely because there is an SVG that could not be parsed
            """
            print(url)
            print("either the image could not be read or the hash could not be added to the database")
            print(e)
            """ if 'transaction block' in e:
                while True:
                    time.sleep(5) """