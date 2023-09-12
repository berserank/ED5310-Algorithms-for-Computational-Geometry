import CGAL
from CGAL.CGAL_Kernel import Point_2
from CGAL.CGAL_Triangulation_2 import Constrained_triangulation_2
from triangulation_ear_clipping import triangulate, Vertex, area_list, Polygon
import matplotlib.pyplot as plt
import time
from polygon_generator import polygons

# Define the polygon vertices in counterclockwise order
polygon_vertices_cgal = [
    Point_2(0, 0),
    Point_2(1, 0),
    Point_2(1, 1),
    Point_2(0, 1),
]


def ear_clipping(single_list):
    if area_list(single_list) < 0:
        single_list.reverse()
    vertex_list = []
    for vertex in single_list:
        temp_vertex = Vertex(vertex[0], vertex[1])
        vertex_list.append(temp_vertex)

    polygon = Polygon(vertex_list)
    polygon.update()
    start = time.time()
    diagonals = triangulate(polygon)
    end = time.time()
    time_taken = end-start
    return time_taken


def cgal(single_list):
    polygon_vertices_cgal = [Point_2(vertex[0],vertex[1]) for vertex in single_list]
    triangulation = Constrained_triangulation_2()

    for vertex in polygon_vertices_cgal:
        triangulation.insert(vertex)

    num_vertices = len(polygon_vertices_cgal)
    time_taken = 0
    for i in range(num_vertices):
        vertex1 = polygon_vertices_cgal[i]
        vertex2 = polygon_vertices_cgal[(i + 1) % num_vertices]
        start = time.time()
        triangulation.insert_constraint(vertex1, vertex2)
        end = time.time()
        time_taken += (end-start)

 
    return time_taken

ear_clipping_times = []
cgal_times = []
i = 0

for single_list in polygons:
    print(f'{i+1} Polygons done')
    ear_clipping_times.append(ear_clipping(single_list))
    cgal_times.append(cgal(single_list))
    i = i+1
indices = range(4,len(ear_clipping_times)+4)
fig,ax = plt.subplots(2)
ax[0].plot(indices,ear_clipping_times)
ax[1].plot(indices,cgal_times)
# plt.legend([r'Ear Clipping Algorithm - O($n^2$)', 'CGAL Triangulation'])
ax[0].set_title(r'Ear Clipping Algorithm - O($n^2$)')
ax[1].set_title('CGAL Triangulation')
plt.show()
