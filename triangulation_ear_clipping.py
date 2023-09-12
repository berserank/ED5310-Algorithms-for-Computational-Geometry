import numpy as np
import copy
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches


class Point():
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Vertex(Point):
    def __init__(self,x,y):
        super().__init__(x, y)
        self.ear = False
        self.next = 0
        self.prev = 0

class Polygon():
    def __init__(self,Vertices):
        self.vertices = Vertices
        self.n = len(self.vertices)
        self.edges = []
    
    def update(self):
        self.n = len(self.vertices)
        for i in range(self.n-1):
            self.edges.append([self.vertices[i],self.vertices[i+1]])
            if i>0:
                self.vertices[i].next = self.vertices[i+1]
                self.vertices[i].prev = self.vertices[i-1]
            elif i == 0:
                self.vertices[i].next = self.vertices[1]
                self.vertices[i].prev = self.vertices[self.n-1]

        self.vertices[self.n-1].prev =  self.vertices[self.n-2]
        self.vertices[self.n-1].next =  self.vertices[0]
        self.edges.append([self.vertices[self.n-1],self.vertices[0]])


def angle(A,B,C):
    x = ( C.x - B.x ) * ( A.x - B.x ) + ( C.y - B.y ) * ( A.y - B.y )
    y = ( C.x - B.x ) * ( A.y - B.y ) - ( C.y - B.y ) * ( A.x - B.x )

    if ( x == 0.0 and y == 0.0 ):
        value = 0.0
        return value

    value = np.arctan2 ( y, x )

    if ( value < 0.0 ):
        value = value + 2.0 * np.pi

    value = 180.0 * value / np.pi

    return value


def area(polygon):
    if (isinstance(polygon, Polygon)):
        vertices = polygon.vertices
    else:
        vertices = polygon
    n = len(vertices)
    area = 0
    for i in range(n-1):
        area += (vertices[i].x)*(vertices[i+1].y)-(vertices[i].y)*(vertices[i+1].x)
    area += (vertices[n-1].x)*(vertices[0].y)-(vertices[n-1].y)*(vertices[0].x)
    return area/2

def area_list(vertices):
    n = len(vertices)
    area = 0
    for i in range(n-1):
        area += (vertices[i][0])*(vertices[i+1][1])-(vertices[i][1])*(vertices[i+1][0])
    area += (vertices[n-1][0])*(vertices[0][1])-(vertices[n-1][1])*(vertices[0][0])
    return area

def left_predicate(A,B,C):
    vertices = [A,B,C]
    polygon = Polygon(vertices)
    if area(polygon) > 0 :
        return 1
    elif area(polygon) == 0:
        return -1
    else:
        return 0

def left_on_predicate(A,B,C):
    vertices = [A,B,C]
    polygon = Polygon(vertices)
    if (area(polygon) >= 0):
        return 1
    else:
        return 0

def proper_intersection(A,B,C,D):
    if (left_predicate(A,B,C) == -1 or left_predicate(A,B,D) == -1 or left_predicate(C,D,A) == -1 or left_predicate(C,D,B) == -1):
        return False
    else:
        return((left_predicate(A,B,C)^left_predicate(A,B,D)) and (left_predicate(C,D,A)^left_predicate(C,D,B)) )
    
def betweeness(A,B,C):
    if left_predicate(A,B,C) != -1:
        return False
    else:
        if (A.x != B.x):
            return (((A.x >= C.x) and (C.x >= B.x)) or ((A.x <= C.x) and (C.x <= B.x)))
        else:
            return (((A.y >= C.y) and (C.y >= B.y)) or ((A.y <= C.y) and (C.y <= B.y)))

def intersection(A,B,C,D):
    if (proper_intersection(A,B,C,D)):
        return True
    elif (betweeness(A,B,C) or betweeness(A,B,D) or betweeness(C,D,A) or betweeness(C,D,B)):
        return True
    else:
        return False

 
def equal_vertex(A,B):
    return bool((A.x == B.x) and (A.y == B.y)) 

def diagonalie(A,B,polygon):
    n = polygon.n
    for edge in polygon.edges:
        vertex1 = edge[0]
        vertex2 = edge[1]
        if (equal_vertex(A,vertex1) == False  
            and equal_vertex(A,vertex2) == False
            and equal_vertex(B,vertex1) == False
            and equal_vertex(B,vertex2) == False
            and intersection(A,B,vertex1,vertex2) == True
            ):
            return False
    return True


def Incone(A,B,polygon):
    for i in range(polygon.n):
        vertex = polygon.vertices[i]
        if (equal_vertex(A,vertex)):
            if (i>0 and i<polygon.n-1):
                A0 = polygon.vertices[i-1]
                A1 = polygon.vertices[i+1]
            elif i == 0:
                A0 = polygon.vertices[polygon.n-1]
                A1 = polygon.vertices[1]
            elif i == polygon.n-1:
                A0 = polygon.vertices[polygon.n-2]
                A1 = polygon.vertices[0]
            break
    if bool(left_on_predicate(A,A1,A0)):
        return bool(left_predicate(A,B,A0) and left_predicate(B,A,A1))
    else:
        return bool(not(left_on_predicate(A,B,A1) and left_on_predicate(B,A,A0)))

def diagonal(A,B,polygon):
    return Incone(A,B,polygon) and Incone(B,A,polygon) and diagonalie(A,B,polygon)


def ear_init(polygon):
    for A in polygon.vertices:
        for i in range(polygon.n):
            vertex = polygon.vertices[i]
            if (equal_vertex(A,vertex)):
                if (i>0 and i<polygon.n-1):
                    A0 = polygon.vertices[i-1]
                    A1 = polygon.vertices[i+1]
                elif i == 0:
                    A0 = polygon.vertices[polygon.n-1]
                    A1 = polygon.vertices[1]
                elif i == polygon.n-1:
                    A0 = polygon.vertices[polygon.n-2]
                    A1 = polygon.vertices[0]
                break
        A.ear = diagonal(A0,A1,polygon)

def triangulate(polygon):
    polygon_copy = copy.deepcopy(polygon)
    ear_init(polygon_copy)
    triangulating_diagonals = []
    while polygon_copy.n > 3 :
        # print('hi'+str(polygon_copy.n))
        for i in range(polygon_copy.n):
            V2 = polygon_copy.vertices[i]
            V3 = V2.next
            V4 = V3.next
            V1 = V2.prev
            V0 = V1.prev
            if V2.ear == True:
                triangulating_diagonals.append((V1, V3))
                
                V1.ear = diagonal(V0,V3,polygon)
                V3.ear = diagonal(V1,V4,polygon)

                polygon_copy.vertices.pop(i)
                polygon_copy.update()
                break

    return triangulating_diagonals


polygons = [
[(-4.840035820401431, 2.4921883251939048), (-2.0628100820577884, -3.272148243602482), (2.9408857565970092, -1.5750782213745556), (3.348259321454887, -0.46485148468792)],
[(-3.1919978129941677, -2.568400228325382), (4.842238811069341, -2.8054959128082175), (4.214131220902375, -2.4097527201945135), (4.31587706429453, -0.723659910099787), (1.1134039755086405, -0.13256107638831188)],
[(0.7043255792909442, 0.6771163322751483), (-3.998808070865732, -0.7669691840155348), (3.7550459164982444, -1.2177478085164108), (3.947910737892855, -0.11557327554123165), (3.7899865103836614, -0.041331594885773745), (1.8445362074858425, -0.007117572056334211)],
[(1.1317381528064363, 5.525755857019334), (-2.831219956738485, 1.767344973226917), (0.756906370796907, -0.8694442091804981), (3.331009326187843, -1.5456158537522966), (0.6140305499106941, -0.04816470754929778), (2.344337665016365, -0.06213732698866402), (3.0502287053890735, -0.051209017068158516)],
[(4.941493223152365, 7.621970315248656), (-3.862926075579534, 0.5098380870616778), (0.7664661605541379, -0.37981767292569263), (4.925608975030146, -0.7164537018555496), (2.0700332922873006, -0.23409632113595474), (4.225948379754133, -0.35927819949386114), (3.342786478322047, -0.11817668811504191), (4.795293057274634, -0.06113381328610539)],
[(2.8400918313238632, 6.916796742495461), (-4.648054355349865, 2.932955957819474), (-0.3081725271860858, 0.15134654719131183), (-1.3965042855665633, -1.095256053370464), (-2.8150848342536223, -5.0716434255380385), (0.9189602270175207, -3.2690595883179467), (4.2594391366843345, -6.184955614541533), (4.891314435925331, -2.126425974128677), (4.8820332564069755, -0.20276013896949402)],
[(1.8362755804834496, 1.5305423661379323), (-0.9168308706767497, -0.39403476776010626), (4.574966661373314, -7.981412199327966), (1.192138333665878, -1.3772047007126678), (2.0723082163040663, -2.039030604274737), (3.736243388575013, -0.6069713112024891), (2.9407199299354176, -0.35909991266577956), (2.8546702384678935, -0.2391279180791862), (1.6253540983349395, -0.027924428299347246), (0.22702883357868464, -0.00075255117089076)],
[(0.12745039375186895, 0.02702406831967014), (3.7119333592150863, 4.927781189739157), (-0.37007399420402487, 0.5431472914220129), (-2.641495663196755, 1.888338849076789), (-2.337860300836381, -2.8592237551014246), (-0.7438118922210091, -6.86925571110046), (1.467450698750092, -15.008959197170089), (3.281237658930088, -10.661593390027766), (1.6857629904781357, -0.7008233827786077), (0.8820831457561157, -0.29151978298642117), (1.6821845493671594, -0.09067327242278816)],
[(4.840916910005484, 6.308333307862829), (-1.5274860468726965, 2.6444493264621096), (-2.373337500809869, 1.7648806814968736), (-2.052098960428033, 0.7623785287971454), (-2.670619433474173, 0.11258307097211137), (-3.920031113736162, -1.8051469219612337), (-3.8647108136571964, -2.533314424039992), (-3.43334186835477, -5.271299873462107), (-0.8890836220650672, -2.3341457593445774), (2.225694126339757, -3.760249108481711), (4.199606686533993, -6.517332640975577), (1.3313881892448647, -0.5615876083291825)],
[(3.5559273531793667, 0.5756917481168955), (0.574318668676142, 0.13089417055345115), (4.376103072663767, 2.696818294718616), (2.4094385356154433, 10.197901286319683), (4.155539812857766, 24.136389235812153), (-0.8867598727085635, 17.020398501223262), (-1.5919618624943932, 4.333275369325929), (-2.9621586750231232, 0.33967762547034386), (-1.6957021808715145, -0.2639203956197356), (-4.2747520990463865, -4.379659391772565), (-3.696905431575904, -4.446377876727312), (4.300254311085127, -11.029046039765667), (4.662996087840588, -9.453926486405045)],
[(0,5),(0.5,6),(1,4),(4,7),(6,5),(4,3),(0,0),(-4,3),(-6,5),(-4,7),(-1,4),(-0.5,6)]
]


def triangulate_and_plot(single_list):
    if area_list(single_list) < 0:
        single_list.reverse()
    vertex_list = []
    for vertex in single_list:
        temp_vertex = Vertex(vertex[0], vertex[1])
        vertex_list.append(temp_vertex)

    polygon = Polygon(vertex_list)
    polygon.update()

    vertices = [(vertex.x,vertex.y) for vertex in polygon.vertices]
    vertices.append((polygon.vertices[0].x,polygon.vertices[0].y))

    vertices_copy = copy.deepcopy(vertices)
    diagonals = triangulate(polygon)
    diagonals_list = []
    for i in range(len(diagonals)):
        diagonals_list.append([(diagonals[i][0].x,diagonals[i][0].y),(diagonals[i][1].x,diagonals[i][1].y)])
    path = mpath.Path(vertices)
    patch = mpatches.PathPatch(path, lw=2,facecolor='white', alpha = 0.5)
    fig, ax = plt.subplots()
    ax.add_patch(patch)

    for diagonal in diagonals_list:
        point_A = diagonal[0]
        point_B = diagonal[1]
        x_A, y_A = point_A
        x_B, y_B = point_B
        ax.plot([x_A, x_B], [y_A, y_B], '-.c')

    plt.show() 

# for i in range(len(polygons)):
#     single_list = polygons[i]
#     triangulate_and_plot(single_list)


