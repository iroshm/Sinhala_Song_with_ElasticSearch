from elasticsearch import Elasticsearch

#get input and search elastic
es = Elasticsearch(HOST="http://localhost",PORT=9200)
es=Elasticsearch()

def generateFiles():
    print("gen files!!")
    res = es.search(index="sinhala_song", body={"size": 1100,"query": {"match_all": {}}})
    print("Got %d Hits:" % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        lyric = hit["_source"]['lyric']
        songname = hit["_source"]['songName']
        artist = hit["_source"]['artist']
        genre = hit["_source"]['genre']
        lyricwriter = hit["_source"]['lyricWriter']
        key = hit["_source"]['key']
        beat = hit["_source"]['beat']
        musicdir = hit["_source"]['musicDirector']

        f1 = open("Boost helpers/song_name.txt", "a", encoding='utf-8')
        f1.write(songname + '\n')
        f1.close()

        f2 = open("Boost helpers/artist.txt", "a", encoding='utf-8')
        f2.write(str(artist) + '\n')
        f2.close()

        f3 = open("Boost helpers/beat.txt", "a", encoding='utf-8')
        f3.write(str(beat) + '\n')
        f3.close()

        f4 = open("Boost helpers/genre.txt", "a", encoding='utf-8')
        f4.write(str(genre) + '\n')
        f4.close()

        f5 = open("Boost helpers/key.txt", "a", encoding='utf-8')
        f5.write(str(key) + '\n')
        f5.close()

        f6 = open("Boost helpers/lyric.txt", "a", encoding='utf-8')
        f6.write(str(lyric) + '\n')
        f6.close()

        f7 = open("Boost helpers/lyricwriter.txt", "a", encoding='utf-8')
        f7.write(str(lyricwriter) + '\n')
        f7.close()

        f8 = open("Boost helpers/musicDirectors.txt", "a", encoding='utf-8')
        f8.write(str(musicdir) + '\n')
        f8.close()
        # open and read the file after the appending:
        #f = open("song_name.txt", "r", encoding='utf-8')
        #print(f.read())


generateFiles()