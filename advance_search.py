from tkinter import *
from elasticsearch import Elasticsearch
from tkinter.scrolledtext import ScrolledText
import sinling
from sinling import SinhalaTokenizer

#get input and search elastic
es = Elasticsearch(HOST="http://localhost",PORT=9200)
es=Elasticsearch()
tokenizer = SinhalaTokenizer()
tokenList = []

intList = []
artistList = []
musicdirList = []
lyricwriterList = []
beatList = []
songNameList = []
new_artistList = []
new_musicdirList = []
new_lyricwriterList = []
genre_list = []


splited_artis_names = []
splited_song_names = []
splited_lyric_writer_names = []
splited_m_dir_names = []
splited_genre_names = []

artistBoost = ['කිව්ව','කියූ','ගැයූ','ගායනය','ගයන','ගයනා','ගැයුව','ගැයු']
lrBoost = ['ලියු','සෑදු','ලිව්ව','රචනා','ලියනු']
dBoost = ['අධ්‍යක්ෂණය','සෑදු']
rank = ['හොඳම','ජනප්‍රියම','ජනප්‍රියතම']

aboosted = "aboosted"
lrboosted = "lrboosted"
dboosted = "dboosted"
isRanked = "isRanked"
genreBoost = "genreBoost"

sDict = {}
aDict = {}
lrDict={}
mdDict={}
genDict = {}

songGuess = ""
artistGuess = ""
lrGuess = ""
mdGuess = ""

boostdict={}

class MyWindow:
    def __init__(self, win):
        self.lbl1=Label(win, text='Enter the song name')
        self.t1=Entry(bd=3)

        self.lbl1.place(x=50, y=50)
        self.t1.place(x=220, y=50)
        self.btn1 = Button(win, text='Search')
        self.b1 = Button(win, text='Search', command=self.search)
        self.b1.place(x=50, y=90)


        self.lbl5  = Label(win, text="lyrics")
        self.st1 = ScrolledText(win, height=6)
        self.lbl5.place(x=40, y=120)
        self.st1.place(x=40, y=150)

        self.lbl6 = Label(win, text="Song Name")
        self.lbl7 = Label(win, text="Artist")
        self.lbl8 = Label(win, text="Genre")
        self.lbl9 = Label(win, text="Lyric Writer")
        self.lbl10 = Label(win, text="Key")
        self.lbl11 = Label(win, text="Beat")
        self.lbl12 = Label(win, text="views")
        self.lbl13 = Label(win, text="shares")
        self.lbl14 = Label(win, text="Music Director")

        self.st6 = ScrolledText(win, height=2);
        self.st7 = ScrolledText(win, height=2);
        self.st8 = ScrolledText(win, height=2);
        self.st9 = ScrolledText(win, height=2);
        self.st10 = ScrolledText(win, height=2);
        self.st11 = ScrolledText(win, height=2);
        self.st12 = ScrolledText(win, height=2);
        self.st13 = ScrolledText(win, height=2);
        self.st14 = ScrolledText(win, height=2);

        self.lbl6.place(x=40, y=250)
        self.st6.place(x=40, y=280)

        self.lbl7.place(x=730, y=250)
        self.st7.place(x=730, y=280)

        self.lbl8.place(x=40, y=340)
        self.st8.place(x=40, y=370)

        self.lbl9.place(x=730, y=340)
        self.st9.place(x=730, y=370)

        self.lbl10.place(x=40, y=430)
        self.st10.place(x=40, y=460)

        self.lbl11.place(x=730, y=430)
        self.st11.place(x=730, y=460)

        self.lbl12.place(x=40, y=520)
        self.st12.place(x=40, y=550)

        self.lbl13.place(x=730, y=520)
        self.st13.place(x=730, y=550)

        self.lbl14.place(x=40, y=610)
        self.st14.place(x=40, y=640)


    def search(self):
        input = self.t1.get()
        processInput(input)


def processInput(input):
    userInput = input
    tokenList =  tokenizer.tokenize(userInput)
    intList = isInt(tokenList)
    checkBoost(tokenList)
    songName = songNameIdentifier(tokenList)
    artistNames = artistIdentifier(tokenList)
    lwname = lwIdentifier(tokenList)
    searchQuery(songName,artistNames,lwname,intList,userInput)


#def priority():
    #lw , artist wage dekk boost unoth length eka wadima eka ganna



def lwIdentifier(tlist):
    lwn = ""
    for i in tlist:
        if i in splited_lyric_writer_names:
            lwn = lwn + i + " "
    return lwn

def songNameIdentifier(tlist):
    sg = ""
    for i in tlist:
        if i in splited_song_names:
            sg = sg + i + " "
    return sg

def artistIdentifier(tlist):
    an = ""
    for i in tlist:
        if i in splited_artis_names:
            an = an + i + " "
    return an

def lwSpliter(lwlist):
    for i in lwlist:
        list = tokenizer.tokenize(i)
        if i not in lrDict.keys():
            lrDict[i] = list
            for k in list:
                splited_lyric_writer_names.append(k)

def genreSpliter(glist):
    for i in glist:
        list = tokenizer.tokenize(i)
        if i not in genDict.keys():
            genDict[i] = list
            for k in list:
                splited_genre_names.append(k)



def artistNSpliter(alist):
    for i in alist:
        list = tokenizer.tokenize(i)
        if i not in aDict.keys():
            aDict[i] = list
            for k in list:
                splited_artis_names.append(k)


def songSpliter(slist):
    for i in slist:
        list = tokenizer.tokenize(i)
        if i not in sDict.keys():
            sDict[i] = list
            for k in list:
                splited_song_names.append(k)

def checkBoost(tlist):
    for i in tlist:
        if i in artistBoost:
            boostdict[aboosted] = True
            print("ab")
        if i in lrBoost:
            boostdict[lrboosted] = True
            print("lb")
        if i in dBoost:
            boostdict[dboosted] = True
            print("db")
        if i in rank:
            boostdict[isRanked] = True
            print("rb")
        if i in splited_genre_names:
            boostdict[genreBoost] = True
            print("gb")



def cleanArray(array):
    lista = []
    for i in array:
        i = i.replace('[', '')
        i = i.replace(']', '')
        i = i.replace("'", '')
        lista.append(i)
    return(lista)

def isInt(tokenList):
    intlist = []
    for i in tokenList:
        try:
            intlist.append(int(i))
        except ValueError:
            err = 1
    return intlist

def getLists():
    filepath = 'Boost helpers/artist.txt'
    with open(filepath, encoding='utf-8-sig') as fp:
        line = fp.readline()
        cnt = 1
        while line:
            artistList.append(line.strip())
            line = fp.readline()
            cnt += 1

    filepath = 'Boost helpers/musicDirectors.txt'
    with open(filepath, encoding='utf-8-sig') as fp:
        line = fp.readline()
        cnt = 1
        while line:
            musicdirList.append(line.strip())
            line = fp.readline()
            cnt += 1

    filepath = 'Boost helpers/lyricwriter.txt'
    with open(filepath, encoding='utf-8-sig') as fp:
        line = fp.readline()
        cnt = 1
        while line:
            lyricwriterList.append(line.strip())
            line = fp.readline()
            cnt += 1

    filepath = 'Boost helpers/beat.txt'
    with open(filepath, encoding='utf-8-sig') as fp:
        line = fp.readline()
        cnt = 1
        while line:
            beatList.append(line.strip())
            line = fp.readline()
            cnt += 1

    filepath = 'Boost helpers/song_name.txt'
    with open(filepath, encoding='utf-8-sig') as fp:
        line = fp.readline()
        cnt = 1
        while line:
            songNameList.append(line.strip())
            line = fp.readline()
            cnt += 1

    filepath = 'Boost helpers/genreBoost.txt'
    with open(filepath, encoding='utf-8-sig') as fp:
        line = fp.readline()
        cnt = 1
        while line:
            genre_list.append(line.strip())
            line = fp.readline()
            cnt += 1




def searchQuery(songName,artistNames,lwname,rankNum,userInput):
    sngName = ""
    aName = ""
    lwName = ""
    rank = 20
    if(len(rankNum)>0):
        rank = rankNum[0]
    userInp = userInput

    ab = False
    lwb = False
    mdb = False
    rb = False
    genb = False

    for j in boostdict:
        if (j==aboosted):
            ab = True

        if (j==lrboosted):
            lwb = True

        if (j==dboosted):
            mdb = True

        if (j==isRanked):
            rb = True

        if (j==genreBoost):
            genb = True

    tokenList = tokenizer.tokenize(userInput)
    newQuery = ""
    for i in tokenList:
        newQuery = newQuery + '*' + i + "*" + ' '

    res = es.search(index="sinhala_sindu_tokenizer", body={"size": 20, "query": {"query_string": {"query": newQuery,
                                                                                      "fields": ["songName", "artist",
                                                                                                 "genre", "lyricWriter",
                                                                                                 "musicDirector", "key",
                                                                                                 "beat", "lyric"],
                                                                                                 "fuzziness": "AUTO"}},
                                                          "aggs": {
                                                              "genre filter": {
                                                                  "terms": {"field": "genre","size": 10
                                                                            }
                                                              },
                                                              "artist filter": {
                                                                  "terms": {
                                                                      "field": "artist",
                                                                      "size": 30
                                                                  }}}})
    print("Got %d Hitss:" % res['hits']['total']['value'])


###########################################################################
    if (rb is True):
        if(ab is True and genb is True):
            print(" rank boosted with artist name  with genre fuzz auto")

            res = es.search(index="sinhala_song_tokenizer", body={"size": rank,   "query": {"bool": {"must": [{"query_string": {"query": newQuery,
                                                                                                                      "fields": ["artist"],
                                                                                                                      "fuzziness": "AUTO"}}],
                                                                                           "should": [{"query_string": {"query": newQuery,
                                                                                                                        "fields": ["genre",
                                                                                                                                   "songName",
                                                                                                                                   "lyric",
                                                                                                                                   "lyricWriter",
                                                                                                                                   "musicDirector"],
                                                                                                                        "fuzziness": "AUTO"}}]}},
                                                        "sort":[{"views": "desc"}]})

            print("Got %d Hits:" % res['hits']['total']['value'])

        elif (ab is True):
            print(" rank boosted with artist name fuzz auto")
            res = es.search(index="sinhala_song_tokenizer",
                            body={"size": rank, "query": {"bool": {"must": [{"query_string": {"query": newQuery,
                                                                                              "fields": ["artist"],
                                                                                              "fuzziness": "AUTO"}}],
                                                                   "should": [{"query_string": {"query": newQuery,
                                                                                                "fields": ["genre",
                                                                                                           "songName",
                                                                                                           "lyric",
                                                                                                           "lyricWriter",
                                                                                                           "musicDirector"],
                                                                                                "fuzziness": "AUTO"}}]}},
                                  "sort": [{"views": "desc"}]})
            print("Got %d Hits:" % res['hits']['total']['value'])

            if (res['hits']['total']['value'] < 1):

                print(" do not have artist name but boosted")

                res = es.search(index="sinhala_song_tokenizer", body={"size": rank, "query": {"query_string": {"query": newQuery,
                                                                                                     "fields": [
                                                                                                         "songName",
                                                                                                         "artist",
                                                                                                         "genre",
                                                                                                         "lyricWriter",
                                                                                                         "musicDirector",
                                                                                                         "key",
                                                                                                         "beat",
                                                                                                         "lyric"],
                                                                                                     "fuzziness": "AUTO"}},
                                                            "sort": [{"views": "desc"}]})
                print("Got %d Hits:" % res['hits']['total']['value'])


        elif(lwb is True and genb is True):
            print(" rank boosted with lwriter name with genre fuzz auto")


            res = es.search(index="sinhala_song_tokenizer",
                            body={"size": rank, "query": {"bool": {"must": [{"query_string": {"query": newQuery,
                                                                                              "fields": ["lyricWriter"],
                                                                                              "fuzziness": "AUTO"}}],
                                                                   "should": [{"query_string": {"query": newQuery,
                                                                                                "fields": ["artist","genre",
                                                                                                           "songName",
                                                                                                           "lyric",
                                                                                                           "musicDirector"],
                                                                                                "fuzziness": "AUTO"}}]}},
                                  "sort": [{"views": "desc"}]})


            print("Got %d Hits:" % res['hits']['total']['value'])

        elif(lwb is True):
            print(" rank boosted with lwriter name fuzz auto")
            res = es.search(index="sinhala_song_tokenizer",
                            body={"size": rank, "query": {"bool": {"must": [{"query_string": {"query": newQuery,
                                                                                              "fields": [
                                                                                                  "lyricWriter"],
                                                                                              "fuzziness": "AUTO"}}],
                                                                   "should": [{"query_string": {"query": newQuery,
                                                                                                "fields": ["artist",
                                                                                                           "genre",
                                                                                                           "songName",
                                                                                                           "lyric",
                                                                                                           "musicDirector"],
                                                                                                "fuzziness": "AUTO"}}]}},
                                  "sort": [{"views": "desc"}]})

            print("Got %d Hits:" % res['hits']['total']['value'])

            if (res['hits']['total']['value'] < 1):

                    print(" do not have lwriter name but boosted fuzz auto")



                    res = es.search(index="sinhala_song_tokenizer", body={"size": rank, "query": {"query_string": {"query": newQuery,
                                                                                                         "fields": [
                                                                                                             "songName",
                                                                                                             "artist",
                                                                                                             "genre",
                                                                                                             "lyricWriter",
                                                                                                             "musicDirector",
                                                                                                             "key",
                                                                                                             "beat",
                                                                                                             "lyric"],
                                                                                                         "fuzziness": "AUTO"}},
                                                                "sort": [{"views": "desc"}]})
                    print("Got %d Hits:" % res['hits']['total']['value'])

        elif(mdb is True and genb is True):
            print(" rank boosted with mdirector name with genb fuzz auto")

            res = es.search(index="sinhala_song_tokenizer",
                            body={"size": rank, "query": {"bool": {"must": [{"query_string": {"query": newQuery,
                                                                                              "fields": [
                                                                                                  "musicDirector"],
                                                                                              "fuzziness": "AUTO"}}],
                                                                   "should": [{"query_string": {"query": newQuery,
                                                                                                "fields": ["artist",
                                                                                                           "genre",
                                                                                                           "songName",
                                                                                                           "lyric",
                                                                                                           "lyricWriter"],
                                                                                                "fuzziness": "AUTO"}}]}},
                                  "sort": [{"views": "desc"}]})

            print("Got %d Hits:" % res['hits']['total']['value'])



        elif(mdb is True):
            print(" rank boosted with mdirector name fuzz auto")
            res = es.search(index="sinhala_song_tokenizer",
                            body={"size": rank, "query": {"bool": {"must": [{"query_string": {"query": newQuery,
                                                                                              "fields": [
                                                                                                  "musicDirector"],
                                                                                              "fuzziness": "AUTO"}}],
                                                                   "should": [{"query_string": {"query": newQuery,
                                                                                                "fields": ["artist",
                                                                                                           "genre",
                                                                                                           "songName",
                                                                                                           "lyric",
                                                                                                           "lyricWriter"],
                                                                                                "fuzziness": "AUTO"}}]}},
                                  "sort": [{"views": "desc"}]})

            print("Got %d Hits:" % res['hits']['total']['value'])

            if (res['hits']['total']['value'] < 1):

                print(" do not have mdirector name but boosted fuzz auto")



                res = es.search(index="sinhala_song_tokenizer", body={"size": rank, "query": {"query_string": {"query": newQuery,
                                                                                                     "fields": [
                                                                                                         "songName",
                                                                                                         "artist",
                                                                                                         "genre",
                                                                                                         "lyricWriter",
                                                                                                         "musicDirector",
                                                                                                         "key",
                                                                                                         "beat",
                                                                                                         "lyric"],
                                                                                                     "fuzziness": "AUTO"}},
                                                            "sort": [{"views": "desc"}]})
                print("Got %d Hits:" % res['hits']['total']['value'])
        else:
            print("only rank boosted fuzz auto")


            res = es.search(index="sinhala_song_tokenizer",
                            body={"size": rank, "query": {"bool": {"must": [{"query_string": {"query": newQuery,
                                                                                              "fields": [
                                                                                                  "lyricWriter","artist","musicDirector"],
                                                                                              "fuzziness": "AUTO"}}],
                                                                   "should": [{"query_string": {"query": newQuery,
                                                                                                "fields": ["artist",
                                                                                                           "genre",
                                                                                                           "songName",],
                                                                                                "fuzziness": "AUTO"}}]}},
                                  "sort": [{"views": "desc"}]})

            print("Got %d Hits:" % res['hits']['total']['value'])

    ############################################################################
    else:
        print("not ranked")
        if (ab is True and genb is True):
            print(" rank not boosted but artist name boosted with genre fuzz auto")

            res = es.search(index="sinhala_song_tokenizer", body={"size": 20, "query": {"query_string": {"query": newQuery,
                                                                                                "fields": [
                                                                                                    "songName",
                                                                                                    "artist",
                                                                                                    "genre",
                                                                                                    "lyricWriter",
                                                                                                    "musicDirector",
                                                                                                    "key",
                                                                                                    "beat",
                                                                                                    "lyric"],
                                                                                               "fuzziness": "AUTO"}}})
            print("Got %d Hits:" % res['hits']['total']['value'])

        elif (ab is True):
            print(" rank not boosted but artist name boosted fuzz auto" )
            res = es.search(index="sinhala_song_tokenizer", body={"size": rank, "query": {"multi_match": {"query": userInput,
                                                                                                "fields": ["songName",
                                                                                                           "artist"],
                                                                                                "fuzziness": "AUTO"}}})
            print("Got %d Hits:" % res['hits']['total']['value'])

            if (res['hits']['total']['value'] < 1):

                print(" do not have artist name do wildcard fuzz auto")

                res = es.search(index="sinhala_song_tokenizer", body={"size": 20, "query": {"query_string": {"query": newQuery,
                                                                                                   "fields": [
                                                                                                       "songName",
                                                                                                       "artist",
                                                                                                       "genre",
                                                                                                       "lyricWriter",
                                                                                                       "musicDirector",
                                                                                                       "key",
                                                                                                       "beat",
                                                                                                       "lyric"],
                                                                                                   "fuzziness": "AUTO"}}})
                print("Got %d Hits:" % res['hits']['total']['value'])

        elif (lwb is True and genb is True):
            print(" rank nor boosted but lwriter name boosted with genb fuzz auto")

            print(" do not have lwriter name do wildcard")

            res = es.search(index="sinhala_song_tokenizer", body={"size": 20, "query": {"query_string": {"query": newQuery,
                                                                                                "fields": [
                                                                                                    "songName",
                                                                                                    "artist",
                                                                                                    "genre",
                                                                                                    "lyricWriter",
                                                                                                    "musicDirector",
                                                                                                    "key",
                                                                                                    "beat",
                                                                                                    "lyric"],
                                                                                               "fuzziness": "AUTO"}}})
            print("Got %d Hits:" % res['hits']['total']['value'])

        elif (lwb is True):
            print(" rank nor boosted but lwriter name boosted fuzz auto")
            res = es.search(index="sinhala_song_tokenizer", body={"size": rank, "query": {"multi_match": {"query": userInput,
                                                                                                "fields": ["lyricWriter"],
                                                                                                "fuzziness": "AUTO"}}})
            print("Got %d Hits:" % res['hits']['total']['value'])

            if (res['hits']['total']['value'] < 1):

                print(" do not have lwriter name do wildcard fuzz auto")



                res = es.search(index="sinhala_song_tokenizer", body={"size": 20, "query": {"query_string": {"query": newQuery,
                                                                                                   "fields": [
                                                                                                       "songName",
                                                                                                       "artist",
                                                                                                       "genre",
                                                                                                       "lyricWriter",
                                                                                                       "musicDirector",
                                                                                                       "key",
                                                                                                       "beat",
                                                                                                       "lyric"],
                                                                                                   "fuzziness": "AUTO"}}})
                print("Got %d Hits:" % res['hits']['total']['value'])

        elif (mdb is True and genb is True):
            print(" rank not boosted but mdirector name boosted with genb fuzz auto")



            res = es.search(index="sinhala_song_tokenizer", body={"size": 20, "query": {"query_string": {"query": newQuery,
                                                                                                "fields": [
                                                                                                    "songName",
                                                                                                    "artist",
                                                                                                    "genre",
                                                                                                    "lyricWriter",
                                                                                                    "musicDirector",
                                                                                                    "key",
                                                                                                    "beat",
                                                                                                    "lyric"],
                                                                                               "fuzziness": "AUTO"}}})
            print("Got %d Hits:" % res['hits']['total']['value'])

        elif (mdb is True):
            print(" rank not boosted but mdirector name boosted fuzz auto")
            res = es.search(index="sinhala_song_tokenizer", body={"size": rank, "query": {"multi_match": {"query": userInput,
                                                                                                "fields": ["musicDirector"],
                                                                                                "fuzziness": "AUTO"}}})
            print("Got %d Hits:" % res['hits']['total']['value'])

            if (res['hits']['total']['value'] < 1):

                print(" do not have mdirector name do wildcard fuzz auto")



                res = es.search(index="sinhala_song_tokenizer", body={"size": 20, "query": {"query_string": {"query": newQuery,
                                                                                                   "fields": [
                                                                                                       "songName",
                                                                                                       "artist",
                                                                                                       "genre",
                                                                                                       "lyricWriter",
                                                                                                       "musicDirector",
                                                                                                       "key",
                                                                                                       "beat",
                                                                                                       "lyric"],
                                                                                                   "fuzziness": "AUTO"}}})
                print("Got %d Hits:" % res['hits']['total']['value'])

    if (res['hits']['total']['value'] < 5):
        print("result not enough")
        if(rb is True):
            res = es.search(index="sinhala_song_tokenizer", body={"size": rank, "query": {"match_all": {}},
                                                        "sort":[{"views": "desc"}]})
            print("Got %d Hits:" % res['hits']['total']['value'])

        else:

            res = es.search(index="sinhala_song_tokenizer", body={"size": 20, "query": {"query_string": {"query": newQuery,
                                                                                              "fields": ["songName",
                                                                                                         "artist",
                                                                                                         "genre",
                                                                                                         "lyricWriter",
                                                                                                         "musicDirector",
                                                                                                         "key",
                                                                                                         "beat",
                                                                                                         "lyric"],
                                                                                               "fuzziness": "AUTO"}}})
            print("Got %d Hits:" % res['hits']['total']['value'])

    MyWindow.__init__(mywin,win=window)
    i = 0
    for hit in res['hits']['hits']:
        i = i + 1
        mywin.st1.insert(END, "result " + str(i) + "---------------------")
        mywin.st1.insert(END, hit["_source"]['lyric'])

        mywin.st6.insert(END, "result " + str(i) + " : ")
        mywin.st6.insert(END, hit["_source"]['songName'] + '\n')

        mywin.st7.insert(END, "result " + str(i) + " : ")
        mywin.st7.insert(END, str(hit["_source"]['artist']) + '\n')

        mywin.st8.insert(END, "result " + str(i) + " : ")
        mywin.st8.insert(END, str(hit["_source"]['genre']) + '\n')

        mywin.st9.insert(END, "result " + str(i) + " : ")
        mywin.st9.insert(END, str(hit["_source"]['lyricWriter']) + '\n')

        mywin.st10.insert(END, "result " + str(i) + " : ")
        mywin.st10.insert(END, str(hit["_source"]['key']) + '\n')

        mywin.st11.insert(END, "result " + str(i) + " : ")
        mywin.st11.insert(END, str(hit["_source"]['beat']) + '\n')

        mywin.st12.insert(END, "result " + str(i) + " : ")
        mywin.st12.insert(END, str(hit["_source"]['views']) + '\n')

        mywin.st13.insert(END, "result " + str(i) + " : ")
        mywin.st13.insert(END, str(hit["_source"]['shares']) + '\n')

        mywin.st14.insert(END, "result " + str(i) + " : ")
        mywin.st14.insert(END, str(hit["_source"]['musicDirector']) + '\n')

getLists()
new_artistList = cleanArray(artistList)
new_musicdirList = cleanArray(musicdirList)
new_lyricwriterList = cleanArray(lyricwriterList)

songSpliter(songNameList)
artistNSpliter(new_artistList)
lwSpliter(new_lyricwriterList)
genreSpliter(genre_list)



window=Tk()
mywin=MyWindow(window)
window.title('Sinhala sindu')
window.geometry("800x900+10+10")

#generateFiles()

window.mainloop()





