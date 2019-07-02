import math

def get_cord(file):
    if file is None:
        return
    reading = file.readline()
    reading = reading[:-1]
    cord = reading.split(",")
    cord[0] = float(cord[0])
    cord[1] = float(cord[1])
    cc = (cord[0], cord[1])
    return cc

def draw_circle(cords,radius,color,canvas):
    canvas.ellipse(tuple(i - radius for i in cords) + tuple(i + radius for i in cords) ,fill=color, outline="blue")


def CheckPoint(bounds, point):
    #    bound = (bounds['width'],bounds['height'])
    status = False
    if point[0] <= bounds['width']:
        status = True
    else:
        return False

    if point[0] >= 0:
        status = True
    else:
        return False

    if point[1] <= bounds['height']:
        status = True
    else:
        return False

    if point[1] >= 0:
        status = True
    else:
        return False
    return status


def CalcPoint(bounds, new_lon, new_lat):
    if type(bounds) is not dict:
        return
    try:
        diff1 = abs(bounds['lon1']-bounds['lon2'])
        diff2 = abs(bounds['lat1']-bounds['lat2'])
        diff_lon = abs(bounds['lon1'] - new_lon)
        diff_lat = abs(bounds['lat2'] - new_lat)
        y = (bounds['height'] * diff_lon) / diff1
        x = (bounds['width'] * diff_lat) / diff2
        return (int(y),int(x))
        # return(100,100)
    except:
        return( 0,0)

# def CalcPoint(bounds, new_lon, new_lat):
#     if type(bounds) is not dict:
#         return
#     try:
#         diff1 = abs(bounds['lon1']-bounds['lon2'])
#         diff2 = abs(bounds['lat1']-bounds['lat2'])
#         diff_lon = abs(bounds['lon2'] - new_lon)
#         diff_lat = abs(bounds['lat2'] - new_lat)
#         y = (bounds['height'] * diff_lon) / diff1
#         x = (bounds['width'] * diff_lat) / diff2
#         return (int(y),int(x))
#     except:
#         return( 0,0)

def CalcAngle(cords, base):
    if type(cords) is not tuple:
        return
    return int(round(math.atan2(cords[0]-base[0],cords[1]-base[0]) * 57.29577951308232))

def cord_convert(lat_str, lon_str):
    if type(lat_str) is not str:
        return
    lat =  float(lat_str[:3] + "." + lat_str[3:])
    lon =  float(lon_str[:3] + "." + lon_str[3:])


def point_point_distance(center,point):
    return abs ( math.sqrt( pow(center[0]-point[0],2) + pow(center[0]-point[0],2) ) )

def GetSin(point,point2):
    diffx = point[1] - point2[1]
    diffy = point[0] - point2[0]
    diffxy = point_point_distance(point,point2)
    print(diffx, diffy, diffxy)
    if diffx == 0 and diffy == 0:
        return 0

    if diffx == 0 and diffy > 0:
        return 0
    if diffx == 0 and diffy < 0:
        return 180

    if diffy == 0 and diffx > 0:
        return +90
    if diffy == 0 and diffx < 0:
        return -90
    sinn = int(round( math.cos( diffx/diffxy ) * 57.29577951308232))
    if diffy > 0 and diffx < 0:
        print(diffx, diffy, diffxy, sinn-90)
        return sinn-90
    if diffy < 0 and diffx > 0:
        print(diffx, diffy, diffxy, sinn+90)
        return sinn+90
    if diffy > 0 and diffx > 0:
        print(diffx, diffy, diffxy, sinn)
        return sinn
    if diffy < 0 and diffx < 0:
        print(diffx, diffy, diffxy, sinn-180)
        return sinn-180


def TupleSwap(tpl):
    return (tpl[1], tpl[0])


def f_liniowa(a,b,new_x):                   # wylicza Y na podstawie podanego wsp A i B oraz wartosci X
    _a = (a[0] - b[0]) / (a[1] - b[1])
    _b = a[0] - (a[1] * _a)
    y = (_a * new_x) + _b
    #print(_a,_b)
    return (int(y),new_x)


def f_liniowa_coeff(a, b):                           # wylicza A i B na podstawie dwoch wspolrzednych (TUPLE!)
    if (a[0] - b[0]) == 0:
        return 4500, 0
    else:
        _a = (a[1] - b[1]) / (a[0] - b[0])
        _b = a[1] - (a[0] * _a)
        return _a, _b
