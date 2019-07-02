import numpy as np
import json
from json import JSONEncoder
#import SingleSquare



def generatingRectangles(fourCornerrs,x_divider,y_divider):
        print(fourCornerrs)
        xx_dim=fourCornerrs[1][0]-fourCornerrs[0][0]
        xy_dim=fourCornerrs[1][1]-fourCornerrs[0][1]
        xx_dim /=x_divider
        xy_dim /=x_divider
        print(xx_dim,xy_dim)

        yx_dim=fourCornerrs[3][0]-fourCornerrs[0][0]
        yy_dim=fourCornerrs[3][1]-fourCornerrs[0][1]
        yx_dim /=y_divider
        yy_dim /=y_divider
        print(yx_dim,yy_dim)
        return(xx_dim,xy_dim,yx_dim,yy_dim)




#for SingleSquare in results:
#        SingleSquare.wypisz()

class MyEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__    



