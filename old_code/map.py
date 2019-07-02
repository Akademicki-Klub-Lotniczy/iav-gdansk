from PIL import Image, ImageDraw
import urllib.request

def map_gen():
    BingMapsKey = "AuB_e7ZcerY3vW1Bat55PqmEqbc6EPFJJ5Zl3WWdlu4v4OgoBP-xWLmXvgMzyXAg"   # secretkey do pobrania kafelka mapy
    mapSize= "200,200"                      # ustawienie rozmiaru mapy do pobrania
    pushpin="51.096887,17.122672;;"   
    zoomLevel = 19                          # zoom (1-19)
    mapMetadata = "1"                       # flaga do pobrania metadanych

    # http request pobierajacy kawalek mapy w JPG
    urlp = "https://dev.virtualearth.net/REST/v1/Imagery/Map/AerialWithLabels?pp="+pushpin+"&ms="+mapSize+"&zoomLevel="+str(zoomLevel)+"&mapsize="+mapSize+"&key="+BingMapsKey
    # http request pobierajacy metadane (rozmiar, koordynaty naroznikow itp..)
    urlpMeta = "https://dev.virtualearth.net/REST/v1/Imagery/Map/AerialWithLabels?pp="+pushpin+"&ms="+mapSize+"&zoomLevel="+str(zoomLevel)+"&mapsize="+mapSize+"&mapMetadata=1&key="+BingMapsKey
    return urlp, urlpMeta

def cords_download():
  
    urlp, urlpMeta = map_gen()
    #Kawalek odpowiedzialny za pobranie koordynat (wyciagnalem je z symulatora pixhawka)
    # try:
    #     f = open("cords.txt", "r")
    # except:
    #     print("nie moge otworzyc pliku")
    #     f = None
    #Subprogram do pobrania mapki
    try:
        contents = urllib.request.urlopen(urlp).read()  # wyslij request
        print("Pobralem mape")                          # jesli sie uda printuj message
        with open("img4.jpg","wb") as output:           # zapisz to co masz w pamieci do pliku (wb - writebinary)
            output.write(contents)
        output.close()                                  # zamknij zapisywany plik
    except:
        print("nie moglem pobrac mapy")                 # jesli jest fuckup to powiedz mi o tym

    # subprogram do pobrania metadanych z kawalka mapki
    try:
        contents = urllib.request.urlopen(urlpMeta).read()  # wyslij request
        print("Pobralem metadane")                          # powiedz czy udalo sie pobrac
        #mapjs = json.loads(contents)                        # odpowiedz jest formatu JSON - tutaj go parsuje
    except:
        print("nie moglem pobrac meta danych")              # anti-fuckup


urlp, urlpMeta = map_gen()
print(urlpMeta)