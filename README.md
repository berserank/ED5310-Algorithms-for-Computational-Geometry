# Polygon Triangulation
Assignment 1 of the course ED5310 at IIT Madras

Aim :  This assignment is on the implementation of the triangulation algorithm (preferably $O(n^2)$ )

This is a modular implementation of polygon triangulation consisting of three parts.

## [Polygon Generator](https://github.com/berserank/Polygon-Triangulation/blob/main/polygon_generator.py)

This piece of code generates the polygon dataset. For a given n number of vertices, We randomly choose angles from $0$ to $2\pi$ and sort them in increasing order. At every angle, we can randomly choose a vertex, thus resulting in a legible convex/non-convex polygon.

Using the function `polygon_generator(n)` we can create a polygon (Convex or Non-Convex) of n vertices. The Ooutput of the said function is a list of n vertices in counter-clock wise order as required by the later modules. One can also visualise the same in the same code using matplotlib based polygon viewer.

## [Triangulation - Ear Clipping Algorithm](https://github.com/berserank/Polygon-Triangulation/blob/main/triangulation_ear_clipping.py)

Ear clipping algorithm can be referred from the book "COMPUTATIONAL GEOMETRY IN C - JOSEPH O'ROURKE" or from [here](https://www.geometrictools.com/Documentation/TriangulationByEarClipping.pdf)

This code consists of the implementation of the ear clipping algorithm as per the book. It's runtime is $O(n^2)$ . This program defines the `Polygon` class which is defined by an ordered set of vertices in counter-clock-wise manner. 
The function `triangulate()` can triangulate any given polygon which is an instance of the `Polygon` class. Similarly, to visualise triangulation, one can make use of the function `triangulate_and_plot()`. Here is an example plot produced.
<p align="center">
<img src="https://github.com/berserank/Polygon-Triangulation/blob/main/Batman.png" alt="Alt Text" width="700" height="400">
</p>

## [Triangulation - CGAL Implementation and Comparison](https://github.com/berserank/Polygon-Triangulation/blob/main/cgal_triangulation.py)

This code contains the CGAL impementation of triangulation using the `Constrained_triangulation_2` class from the `CGAL` library. We compare the runtimes of both the implementations for polygons of sizes 4 to 200. Plot is attached below.

<p align="center">
<img src="https://github.com/berserank/Polygon-Triangulation/blob/main/Comparison.png" alt="Alt Text" width="600" height="800">
</p>

