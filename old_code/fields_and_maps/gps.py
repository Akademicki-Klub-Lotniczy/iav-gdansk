from bingmaps.apiservices import LocationByPoint
#import responses
import urllib.request
import json
from PIL import Image, ImageDraw
from geoutils import *
from geopy import distance
# from dropplace import *
# from opener import *


def map_gen():
    BingMapsKey = "AuB_e7ZcerY3vW1Bat55PqmEqbc6EPFJJ5Zl3WWdlu4v4OgoBP-xWLmXvgMzyXAg"   # secretkey do pobrania kafelka mapy
    mapSize= "450,450"                      # ustawienie rozmiaru mapy do pobrania
    pushpin="54.370418,18.630057;;"       # koordynata srodka kafelka (cel do zrzutu)
    zoomLevel = 19                          # zoom (1-19)
    mapMetadata = "1"                       # flaga do pobrania metadanych

    # http request pobierajacy kawalek mapy w JPG
    urlp = "https://dev.virtualearth.net/REST/v1/Imagery/Map/AerialWithLabels?pp="+pushpin+"&ms="+mapSize+"&zoomLevel="+str(zoomLevel)+"&mapsize="+mapSize+"&key="+BingMapsKey
    # http request pobierajacy metadane (rozmiar, koordynaty naroznikow itp..)
    urlpMeta = "https://dev.virtualearth.net/REST/v1/Imagery/Map/AerialWithLabels?pp="+pushpin+"&ms="+mapSize+"&zoomLevel="+str(zoomLevel)+"&mapsize="+mapSize+"&mapMetadata=1&key="+BingMapsKey
    return urlp, urlpMeta


def cords_download():
    urlp, urlpMeta = map_gen()
    # Kawalek odpowiedzialny za pobranie koordynat (wyciagnalem je z symulatora pixhawka)
    try:
        f = open("cords.txt", "r")
    except:
        print("nie moge otworzyc pliku")
        f = None

    # Subprogram do pobrania mapki
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
        #print(contents)
        mapjs = json.loads(contents)                        # odpowiedz jest formatu JSON - tutaj go parsuje
        resources = mapjs["resourceSets"][0]["resources"][0]    # przepisuje odpowiednie drzewko JSON z odpowiedzi (pomijam smieci)
        print(resources)                                    # pokaz mi co jest w odpowiedzi
    except:
        print("nie moglem pobrac meta danych")              # anti-fuckup

    if resources:                                           # jesli cos jest w zmiennej
        bound = dict([                                      # robimy JSONa mowiacego o naroznikach
            ('lat1', resources["bbox"][0]),                 # czytam z responsa LAT w punkcie (0,0)
            ('lon1', resources["bbox"][1]),                 # czytam z responsa LON w punkcue (0,0)
            ('lat2', resources["bbox"][2]),                 # czytam z responsa LAT w punkcie (x,y)
            ('lon2', resources["bbox"][3]),                 # czytam z responsa LAT w punkcie (x,y)
            ('height', int(resources["imageWidth"]) ),      # czytam z reponsa jaka jest szerokosc (powyzsze x) obrazka
            ('width',  int(resources["imageHeight"]) )      # czytam z responsa jaka jest wysokosc (powyzsze y) obrazka
        ])
        point = dict([                                      # robimy JSONa mowiacego o pozycji punktu srodkowego
            ('lat', float(resources["pushpins"][0]["point"]["coordinates"][0])),    # lat
            ('lon', float(resources["pushpins"][0]["point"]["coordinates"][1]))     # lon
        ])
        #DEBUG!!
        print(bound)    # pokaz co masz w JSON bound
        print(point)    # pokaz co masz w JSON point
        CalcPoint(bound, point['lon'], point['lat'] )
        return bound, point, f


def bcg_gen():
    '''Funkcja generująca tło z celem'''
    bound, point, f = cords_download()
    #PILOW - BIBLIOTEKA DO TWORZENIA OBRAZKOW
    im = Image.open("img4.jpg")         #   wczytaj oryginalny pobrany obrazek
    plane = Image.open("plane.png")     #   wczytaj ikonke samolotu
    plane = plane.resize((50, 50))       #   przeskaluj ikonke samolotu do wymiaru (50,50)

    # przekonwertuj wspolrzedne srodka mapy (zalozonego celu) na wspolrzedne obrazka
    target = CalcPoint(bound, point['lon'], point['lat'])

    # utworz obiekt ktory zawiera przezroczysty kanal (merge)
    merge = Image.new("RGBA", (900, 900))

    # wklej wczytany obrazek jako wartstwe do obiektu ^merge
    merge.paste(im, (0, 0))

    # utworz wartwe w obiekcie merge (nazwa wartswy draw)
    draw = ImageDraw.Draw(merge)

    # narysuj na warstwie draw kolko ( (x,y), promien, kolor, warstwa docelowa )
    draw_circle(target, 15, "blue", draw)
    draw_circle(target, 5, "white", draw)
    bcg = merge.save('static/background.png')
    return target, bound, point, f, bcg


def illustrator(n:int ):
    '''funkcja rysująca jedynie położenie samolotu i punktu zrzutu narfa i wody. Przyjmowany argument to ilość punktów
       jakie ma odczytać z pliku'''
    target, bound, point, f, bcg = bcg_gen()

    merge = Image.new("RGBA", (900, 900))
    draw = ImageDraw.Draw(merge)

    prev_cords = (0, 0)                                          # anti fuckup
    new_dest2 = (0, 0)                                           # anti fuckup
    main_cords = []
    cords = []                                                  # potrzebne do wyliczania funkcji liniowej
    nerf_drop = []
    water_drop = []
    for i in range (0, n):        # wczytuje n linijek z pliku
        prev_dest = new_dest2                                       # zapamietaj poprzednia iteracje
        new_cord = get_cord(f)                                      # pobierz koordynate z pliku (f)
        new_dest2 = CalcPoint(bound, new_cord[1], new_cord[0])       # przeksztalc koordynate na punkt
        main_cords.append(new_cord)
        cords.append(new_dest2)


    area_instance = StrefaZrzutu()
    '''Tutaj ważne jest by prędkość wiatru była wynikiem odejmowania prędkośći samolotu z pixa i prędkości z gps'''
    for j in range(len(cords) - 2):
        _a, _b = f_liniowa_coeff(cords[j], cords[j + 1])
        nerf_drop_cord = area_instance.wspolrzedne_zrzutu(xs=cords[j + 1][0], ys=cords[j + 1][1], vs=30, hs=30, a=_a,
                                                     vw=5, B=0, m=0.132, s=0.01935, cords=cords, j=j)
        nerf_drop.append(nerf_drop_cord)

        water_drop_cord = area_instance.wspolrzedne_zrzutu(xs=cords[j + 1][0], ys=cords[j + 1][1], vs=30, hs=30, a=_a,
                                                          vw=5, B=0, m=0.52, s=0.01175, cords=cords, j=j)
        water_drop.append(water_drop_cord)

        water = open_clap(target[0], target[1], water_drop_cord[0], water_drop_cord[1], 15)
        nerf = open_clap(target[0], target[1], nerf_drop_cord[0], nerf_drop_cord[1], 15)

        if water is True and nerf is True:
            print('Otwieram klapę')

    #merge.alpha_composite(plane.rotate( CalcAngle(new_dest2,target) ),dest=tuple(i-25 for i in new_dest2))  # rysuje samolot obrocony o wyliczony kat miedzy dwoma punktami
    for k in range(len(water_drop)):
        draw_circle(cords[k], 2, "white", draw)                       # narysuj kolko
        draw_circle(water_drop[k], 2, "red", draw)                         # wskaz miejsce zrzutu wody
        draw_circle(nerf_drop[k], 2, "yellow", draw)                          # wskaz miejsce zrzutu nerfa
        draw.line(target+cords[k], fill=20)                         # narysuj linie ()
    #print(drop[k], cords[k], k, main_cords[k])


    # merge.alpha_composite(plane.rotate(CalcAngle(new_dest2,target) ),dest=tuple(i-25 for i in new_dest2))  # rysuje samolot obrocony o kat
    # draw.line(target+new_dest2,fill=60)     # rysuje linie z targetu do samolotu
    draw.text((10, 10), "ANGLE: "+str(CalcAngle(new_dest2, target)), fill=(255, 255, 0))
    draw.text((10, 25), "DISTANCE: "+str(distance.distance((point['lat'], point['lon']), new_cord).meters), fill=(255, 255, 0))

    #merge.alpha_composite(draw)
    front = merge.save("static/imagetestx2D.png")  # zapisz wartstwy do pliku
    return front



if __name__ == '__main__':
    bcg_gen()