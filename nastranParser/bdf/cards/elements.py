#import sys
#from numpy import array,cross,dot
#from numpy import array
#from numpy.linalg import norm

# my code
from AirQuick.general.generalMath import Area,Triangle_AreaCentroidNormal,Normal
from baseCard import Element

from elementsBars  import *
from elementsRigid import *
from elementsShell import *
from elementsSolid import *

class CELAS1(Element):
    type = 'CELAS1'
    def __init__(self,card):
        Element.__init__(self,card)
        self.id  = card.field(1)
        nids = [card.field(3),card.field(5)]
        self.prepareNodeIDs(nids)
        assert len(self.nodes)==2

        ## property ID
        self.pid = card.field(2,self.id)

        ## component number
        self.c1 = card.field(4)
        self.c2 = card.field(5)

    def __repr__(self):
        fields = [self.type,self.eid,self.pid,self.nodes[0],self.c1,self.nodes[1],self.c2]
        return self.printCard(fields)

class CELAS2(Element):
    type = 'CELAS2'
    def __init__(self,card):
        self.id  = card.field(1)
        nids = [card.field(3),card.field(5)]
        self.prepareNodeIDs(nids)
        assert len(self.nodes)==2

        ## stiffness of the scalar spring
        self.k   = card.field(2)

        ## component number
        self.c1 = card.field(4)
        self.c2 = card.field(5)
        
        ## damping coefficient
        self.ge = card.field(6)
        
        ## stress coefficient
        self.s  = card.field(7)

    def __repr__(self):
        fields = [self.type,self.eid,self.pid,self.nodes[0],self.c1,self.nodes[1],self.c2,self.ge,self.s]
        return self.printCard(fields)

class CSHEAR(Element):
    type = 'CSHEAR'
    def __init__(self,card):
        Element.__init__(self,card)
        nids = card.fields(3,7)
        self.prepareNodeIDs(nids)
        assert len(self.nodes)==4

    def __repr__(self):
        fields = [self.type,self.eid,self.pid]+self.nodes
        return self.printCard(fields)

class CRAC2D(Element):
    type = 'CRAC2D'
    def __init__(self,card):
        Element.__init__(self,card)

        nids = card.fields(3,21) # caps at 18
        self.prepareNodeIDs(nids)
        assert len(self.nodes)==18

    def __repr__(self):
        fields = [self.type,self.eid,self.pid]+self.nodes
        return self.printCard(fields)

class CRAC3D(Element):
    type = 'CRAC3D'
    def __init__(self,card):
        Element.__init__(self,card)

        nids = card.fields(3,67) # cap at +3 = 67
        self.prepareNodeIDs(nids)
        assert len(self.nodes)==64

    def __repr__(self):
        fields = [self.type,self.eid,self.pid]+self.nodes
        return printCard(fields)
        
class CVISC(CROD):
    type = 'CVISC'
    def __init__(self,card):
        CROD.__init__(self,card)
    ###
###

class CONM2(Element): # v0.1 not done
    type = 'CONM2'
    # 'CONM2    501274  11064          132.274'
    def __init__(self,card):
        Element.__init__(self,card)
        #self.nids  = [ card[1] ]
        #del self.nids
        self.pid = None
        self.dunno = card.field(2)
        self.blank = card.field(3)
        self.mass  = card.field(4)
        
        #print "nids       = ",self.nids
        #print 'self.dunno = ',self.dunno
        #print 'self.blank = ',self.blank
        #print "mass       = ",self.mass
        #print "card       = ",card
        #print str(self)
        #sys.exit()
    
    def __repr__(self):
        fields = [self.type,self.eid,self.dunno,self.blank,self.mass]
        #fields = [self.type,self.eid,self.blank,self.mass]
        return printCard(fields)

   
