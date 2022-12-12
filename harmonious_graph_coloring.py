# https://pw20we.cs.put.poznan.pl/doku.php?id=start
import igraph as ig
import random

def G(n, p):
    edges = []
    for i in range(1, n):
        for j in range(i):
            if random.random() <= p:
                edges.append([i,j])
    return edges

def visualize(edges, vertices_colors, file_name):
    color_list = ["blue", "red", "cyan", "pink", "green", "purple", "black", "white", "orange", "yellow", "gray"]
    graph = ig.Graph(edges=edges)
    layout = graph.layout_circle()
    ig.plot(
        graph,
        layout=layout,
        target=file_name,
        vertex_color=[color_list[i] for i in vertices_colors]
        )

def main():
    print("Podaj n i p")
    n = int(input()) 
    p = float(input())
    n=6
    edges = G(n,p)
    vertices_colors = greedyHarmoniousColoring(n,edges)
    visualize(edges,vertices_colors,"greedy.png")
    vertices_colors = randomizedGreedyHarmoniousColoring(n,edges)
    visualize(edges,vertices_colors,"random.png")
    vertices_colors = [-1 for i in range(n)]
    for number_of_colors in range(1,n+1):
        optimal = optimalBacktrackingHarmoniousColoring(0,edges,vertices_colors,number_of_colors)
        if optimal != False:
            visualize(edges,optimal,"optimal.png")
            return
    
def optimalBacktrackingHarmoniousColoring(v,edges,vertices_colors,number_of_colors):
    if not -1 in vertices_colors:
        return vertices_colors
    
    for i in range(number_of_colors):
        if (isSafeColoring(v,edges,vertices_colors,i)):
            vertices_colors[v] = i
            if (optimalBacktrackingHarmoniousColoring(v+1,edges,vertices_colors,number_of_colors)):
                return vertices_colors
            vertices_colors[v] = -1
    return False

def isSafeColoring(v,edges,vertices_colors,color):
    banned_colors = []
    chosen_vertex_pairs = []
    banned_pairs = []
    for edge in edges:
        neigh = []
        if edge[0] == v:
            neigh = edge[1]
            if vertices_colors[edge[1]] != -1:
                banned_colors.append(vertices_colors[edge[1]])
                chosen_vertex_pairs.append(edge)
        if edge[1] == v:
            neigh = edge[0]
            if vertices_colors[edge[0]] != -1:
                banned_colors.append(vertices_colors[edge[0]])
                chosen_vertex_pairs.append(edge)
        for edge_neigh in edges:
            if edge_neigh[0] == neigh and vertices_colors[edge_neigh[1]] != -1:
                banned_colors.append(vertices_colors[edge_neigh[1]])
            if edge_neigh[1] == neigh and vertices_colors[edge_neigh[0]] != -1:
                banned_colors.append(vertices_colors[edge_neigh[0]])
        if (vertices_colors[edge[0]] != -1 and vertices_colors[edge[1]] != -1):
            pair = [vertices_colors[edge[0]], vertices_colors[edge[1]]]
            if pair and pair.reverse() not in banned_pairs:
                banned_pairs.append(pair)
    if color in banned_colors:
        return False
    for pair in chosen_vertex_pairs:
        if ([color, vertices_colors[pair[1]]] in banned_pairs
            or [vertices_colors[pair[1]], color] in banned_pairs
            or [color, vertices_colors[pair[0]]] in banned_pairs
            or [vertices_colors[pair[0]], color] in banned_pairs):
            return False
    return True

def randomizedGreedyHarmoniousColoring(n,edges):
    vertices_colors = [-1 for i in range(n)]
    vertices_priority = [[i,0] for i in range(n)]
    for vertex in vertices_priority:
        vertex[1] = random.randint(0,n-1)
    vertices_priority.sort(key=lambda x: -x[1])
    for vertex in vertices_priority:
        v = vertex[0]
        color = random.randint(0,n-1)
        while isSafeColoring(v, edges, vertices_colors, color) == False:
            color += 1
        vertices_colors[v] = color
    return vertices_colors

def greedyHarmoniousColoring(n,edges):
    vertices_colors = [-1 for i in range(n)]
    vertices_degrees = [[i,0] for i in range(n)]
    # sortowanie wierzchołków nierosnąco względem stopnia
    for edge in edges:
        vertices_degrees[edge[0]][1] += 1
        vertices_degrees[edge[1]][1] += 1
    vertices_degrees.sort(key=lambda x: -x[1])
    # kolorowanie zachłanne (pierwszym dozwolonym kolorem)
    for vertex in vertices_degrees:
        v = vertex[0]
        color = 0
        while isSafeColoring(v,edges,vertices_colors,color) == False:
            color += 1
        vertices_colors[v] = color
    return vertices_colors

main()
