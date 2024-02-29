import uuid
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage
from collections import defaultdict


class SongDatabase:
    def __init__(self, db_path):
        self.db = TinyDB(db_path)



    def __contains__(self, filename):

        """Überprüft, ob ein Pfad bereits in der Datenbank registriert wurde."""

        Song = Query()
        return self.db.contains(Song.song_id == self._get_song_id(filename))
    



    def store_song(self, hashes, song_info):

        """Registriert einen Song in der Datenbank."""
        
        if not hashes:

            # Fehlerbehandlung hier einfügen

            return
        

        insert_info = [i if i is not None else "Unknown" for i in song_info]
        for h in hashes:
            self.db.insert({'hash': h[0], 'offset': h[1], 'song_id': h[2], 'artist': insert_info[0], 'album': insert_info[1], 'title': insert_info[2]})
        #self.db.insert({'artist': insert_info[0], 'album': insert_info[1], 'title': insert_info[2], 'song_id': hashes[0][2]})




    def get_matches(self, hashes, threshold=5):

        """Gibt übereinstimmende Songs für eine Reihe von Hashes zurück."""

        h_dict = {h[0]: h[1] for h in hashes}
        #results = self.db.search(Query().hash.one_of(h[0] for h in hashes))
        results = list()
        for _h in hashes:
            res = self.db.search(Query().hash == _h[0])
            results.extend(res)

        result_dict = defaultdict(list)
        for r in results:
            result_dict[r['song_id']].append((r['offset'], h_dict[r['hash']]))
        return result_dict




    def get_info_for_song_id(self, song_id):

        """Sucht Songinformationen für eine gegebene ID."""

        Song = Query()
        result = self.db.get(Song.song_id == song_id)
        print(f"{result=}")
        if result is not None:
            return result['artist'], result['album'], result['title']
        
        return None


    def _get_song_id(self, filename):
        return str(uuid.uuid5(uuid.NAMESPACE_OID, filename).int)
