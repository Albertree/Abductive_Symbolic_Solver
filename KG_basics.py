from matplotlib import colors    ### 까만 노드 인력척력 djqt는 버전 + grid_to_graph_woblack 함수 추가 + 1.414 주석처리 + np array 로 변경
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN # conda install -c conda scikit-learn
import pandas as pd # conda install pandas

cmap = colors.ListedColormap(
        [
            '#000000', # 0 검은색
            '#0074D9', # 1 파란색
            '#FF4136', # 2 빨간색
            '#2ECC40', # 3 초록색
            '#FFDC00', # 4 노란색
            '#AAAAAA', # 5 회색
            '#F012BE', # 6 핑크색
            '#FF851B', # 7 주황색
            '#7FDBFF', # 8 하늘색
            '#870C25', # 9 적갈색
            '#505050', # 10 검은색_select
            '#30A4F9', # 11 파란색_select
            #'#FF4136', 
            '#FF7166', # 12 빨간색_select
            '#5EFC70', # 13 초록색_select
            '#FFFC30', # 14 노란색_select
            '#DADADA', # 15 회색_select
            '#F042EE', # 16 핑크색_select
            '#FFB54B', # 17 주황색_select
            '#AFFBFF', # 18 하늘색_select
            '#B73C55'  # 19 적갈색_select
        ])
    #norm = colors.Normalize(vmin=0, vmax=9)
norm = colors.Normalize(vmin=0, vmax=19)

class Pnode :
    def __init__(self, grid, i, j):
        self.color = grid[i][j]
        self.number = self.node_number(len(grid[0]), i, j)
        self.visual_coord = [3 * j, 3 * (len(grid) - i - 1)]  ## coordinate for visualize
        self.coordinate = [j,i]         ## coordinate from the grid
        self.input = 0
        self.output = 0
        self.type = "Pnode"
    def node_number (self, col, i, j): ## start from 0 to (col * row -1) # may not needed
        temp = i * (col) + j
        return temp
    def __str__(self):
        if self.input == 1:
            return f"Pnode: N:{self.number}, I"
        else :
            return f"Pnode: N:{self.number}, O"
        
class Onode:
    def __init__(self, obj, condition):
        Pnode_list = []
        color_set = set()
        number_set = set()
        for Pnode in obj:
            Pnode_list.append(Pnode)
            color_set.add(Pnode.color)
            number_set.add(Pnode.number)
        self.Pnode_list = Pnode_list
        self.color = color_set            ##questionalbe 
        self.number = number_set  
        self.coordinate = [0,0]
        self.input = 0
        self.output = 0
        self.type = "Onode"
        self.condition = condition
        # [get_coordinate(node) for node in get_center_nodes]    ##questionalbe -> need bbox function first and type will be {(int, int), (int, int) ...}
    def __str__(self):
        pnodes = []
#        for pnode in self.Pnode_list:
#            pnodes.append(pnode.__str__())
        if self.input == 1:
            return f"Onode: N:{self.number}, I"
        else :
            return f"Onode: N:{self.number}, O"
    
class Gnode:
    def __init__(self, node_list): # node_list should contain all the Pnode and Onode from the grid
        self.Node_list = node_list
        color_s = set()
        Pnode_list = []
        Onode_list = []
        for n in node_list:
            if isinstance(n, Pnode):
                color_s.add(n.color)
                Pnode_list.append(n)
            elif isinstance(n, Onode):
                Onode_list.append(n)
        self.color = color_s
        self.Pnode_list = Pnode_list
        self.Onode_list = Onode_list
        self.coordinate = [0,0]
        self.number = 0
        self.input = 0
        self.output = 0
        self.type = "Gnode"
        self.condition = "Gnode"
        # [get_coordinate(node) for node in get_center_nodes]       ## questionable # do we need coornidate for Gnode?
    def __str__(self):
        if self.input == 1:
            return f"Gnode: N:{self.number}, I"
        else :
            return f"Gnode: N:{self.number}, O"

class Vnode:
    def __init__(self, Gnode1, Gnode2): # node_list should contain all the Pnode and Onode from the grid
        self.Gnode_list = [Gnode1, Gnode2]
        self.type = "Vnode"
        self.input = 0
        self.output = 0
        self.color = Gnode1.color.union(Gnode2.color)
        self.Onode_list = [node for node in Gnode1.Onode_list] + [node for node in Gnode2.Onode_list]
        self.Pnode_list = [node for node in Gnode1.Pnode_list] + [node for node in Gnode2.Pnode_list]
    def __str__(self):
        return f"Vnode"

    
class Edge:
    def __init__(self, tag, node1, node2 = None):
        if node2 == None :
            self.node_set = [node1]
        else :
            self.node_set = [node1, node2]
        self.tag = tag       
    def __str__(self):
        n_set = []
        for n in self.node_set:
            n_set.append(n.__str__())
        return f"{n_set, self.tag}"    

def Grid_to_Img(grid): ## function for visualize the image, this function is not a DSL
    plt.axis("off")
    plt.imshow(grid, cmap = cmap, norm = norm)

def Make_NodeList (grid):     ## this function now generate Pnode list from grid
    node_list = []
    if type(grid[0]) == list :
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                temp_node = Pnode(grid, i, j)
                temp_node.color = grid[i][j]
                node_list.append(temp_node)
    return node_list

def Concat_node_list (node_list1, node_list2):
    return node_list1 + node_list2

def Make_Onode (node_list, color_same, dist_dsl, edge_list):
    condition = []
    def edge_list_to_graph(edges):
        graph = {}
        for edge in edges:
            node1, node2 = edge.node_set
            if node1 not in graph:
                graph[node1] = []
            if node2 not in graph:
                graph[node2] = []
            graph[node1].append(node2)
            graph[node2].append(node1)
        return graph
    
    if color_same == True:
        same_color = lambda x1, x2 : True if x1.color == x2.color else False
        node_list1 = node_list
        condition.append("single_color")
    else :
        same_color = lambda x1, x2 : True
        condition.append("multi_color")
        node_list1 = get_background_color_removed(node_list)
    if dist_dsl != None:
        dist_1 = lambda x1, x2 : True if dist_dsl(x1, x2) == 1 else False
        condition.append(dist_dsl.__name__)
    else :
        dist_1 = lambda x1, x2 : True
        condition.append("no_distance")
    same_color_and_dist1 = lambda x1, x2: True if (same_color(x1,x2) == True and dist_1(x1,x2) == True) else False
    s_d_edge_list = Make_edge_list(node_list1, same_color_and_dist1)
    graph = edge_list_to_graph(s_d_edge_list)

    condition = tuple(condition)
    tag = ("get_onode", condition)

    for node in node_list1:
        # if isinstance(node, Onode):
        #     continue
        if node not in graph.keys():
            graph[node] = []
    
    def cluster_graph(graph):
        clusters = []
        visited = set()

        def dfs(node, cluster):
            visited.add(node)
            cluster.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    dfs(neighbor, cluster)

        for node in graph:
            if node not in visited:
                new_cluster = set()
                dfs(node, new_cluster)
                clusters.append(new_cluster)
                
        return clusters

    clusters = cluster_graph(graph)

    Onode_list = []
    # tag = ("get_onode", None)
    for obj in clusters:
        onode = Onode(obj, condition)
        Onode_list.append(onode)
        for pnode in obj:
            e = Edge(tag, pnode, onode)
            edge_list.append(e)



    return Onode_list, edge_list 

def Make_Gnode (node_list, edge_list):
    gnode = Gnode(node_list)
    gnode_list = []
    tag = ("get_gnode", None)
    for node in node_list:
        e = Edge(tag, gnode, node)
        edge_list.append(e)
    gnode_list.append(gnode)
    return node_list + gnode_list, edge_list

def Make_Vnode (node_list, edge_list):
    gnode_list = []
    for n in node_list:
        if isinstance(n, Gnode):
            gnode_list.append(n)
    assert len(gnode_list) == 2
    vnode = [Vnode(gnode_list[0], gnode_list[1])]
    tag = ("get_vnode", None)
    e1 = Edge(tag, vnode[0], gnode_list[0])
    e2 = Edge(tag, vnode[0], gnode_list[1])
    edge_list.append(e1)
    edge_list.append(e2)
    return node_list + vnode, edge_list

def create_edge_list ():
    return []


    
def create_edge (get_dsl, node1, node2):   ## no self connecting edge
    is_dsl = get_to_is(get_dsl) 
    result = is_dsl(node1, node2)   ## result = (bool (dsl_name, taget))
    if result[0] == False :
        return None
    else :
        tag = result[1]
        edge = Edge(tag, node1, node2)
        return edge



def Make_edge_list (node_list, dsl) :
    edge_list = create_edge_list()
    try :
        if isinstance (dsl(node_list[0]), bool) == True: ## dsl is is_dsl with only one param
            # print("dsl is returning bool type with 1 param")
            tag = (dsl.__name__, None)
            for n1 in node_list:
                if dsl(n1) == True :
                    e = Edge(tag, n1, n1)
                    edge_list.append(e)
            return edge_list
        else :
            pass
    except :
        pass
    try :
        if isinstance (dsl(node_list[0], node_list[0]), bool) == True : ## dsl is is_dsl with two param
            # print("dsl is returning bool type with 2 param")
            tag = (dsl.__name__, None)
            for n1 in node_list:
                for n2 in node_list:
                    if dsl(n1, n2) == True and n1 != n2 :
                        e = Edge(tag, n1, n2)
                        edge_list.append(e)
            return edge_list
    except: 
        pass
    ## dsl is get_dsl
    # print("dsl is get_dsl")
    for n1 in node_list:
        for n2 in node_list:
            e = create_edge(dsl, n1, n2)
            if e != None and n1 != n2:
                edge_list.append(e)
                # print(e)
    return edge_list

def Concat_edge_list (edge_list1, edge_list2):
    return edge_list1 + edge_list2

def get_to_is (get_f):
    param_num = get_f.__code__.co_argcount
    dsl_name = get_f.__name__
    if param_num == 2:
        is_dsl = lambda x1, x2 : (
            (True, (dsl_name, get_f(x1, x2))) 
            if x1 != x2 and get_f(x1, x2) != None
            else (False, None)
            )## (bool (name, taget))
        
    elif param_num == 1:
        is_dsl = lambda x1, x2: (
            (True, (dsl_name, get_f(x1))) 
            if (
                get_f(x1) == get_f(x2) and get_f(x1) != None
                and x1 != x2 
            )
            else (
                (True, (dsl_name, None)) if (isinstance(get_f(x1), list) and x2 in get_f(x1))
                else (False, None)
            )
        )
    else :
        print("exception has occured")
        return
    return is_dsl

def node_list_numbering (node_list, i):
    if i == 0: ## input
        for n in node_list:
            if isinstance(n, Gnode):
                n.number = 1
            n.input = 1
            n.output = 0
    else : # output
        for n in node_list:
            if isinstance(n, Gnode):
                n.number = 2
            n.input = 0
            n.output = 1

def visualize(node_list, edge_list, tag):
    x = []
    y = []
    colors = []
    num_nodes = len(node_list)
    for ele in (node_list):
        x.append(ele.visual_coord[0])
        y.append(ele.visual_coord[1])
        colors.append(ele.color)
    for i in range(len(node_list)):
        plt.text(x[i] - 0.1, y[i]- 0.1, node_list[i].number , size = 15, color = 'white')

    for i in range(num_nodes) :
        for j in range(i, num_nodes) :
            for edge in edge_list:
                if edge.node_set == {node_list[i], node_list[j]} and edge.tag == tag:
                    plt.plot([x[i], x[j]], [y[i], y[j]], color = 'black', linewidth = 3)
    plt.axis('off')
    plt.axis('equal')
    plt.scatter(x, y, s = 500, c = colors, cmap = cmap, norm = norm)
    plt.show()




#P-layer DSLs  ########################################################
def get_color_of_node(node):   
    if isinstance(node, Vnode):
        return None
    # if node.color == 0:
    #     return None
    return node.color
def get_horizontal_index(node):  
    if isinstance(node, Pnode):
        return node.coordinate[1]
    else :
        return None
def get_vertical_index(node):    
    if isinstance(node, Pnode):
        return node.coordinate[0]
    else: 
        return None
def get_polar_distance(node1, node2):  
    if isinstance(node1, Pnode) and isinstance(node2, Pnode):
        x = abs(node1.coordinate[0] - node2.coordinate[0])
        y = abs(node1.coordinate[1] - node2.coordinate[1])
        return x if x > y else y
    else :
        return None
def get_manhattan_dist (node1,node2) :     
    if isinstance(node1, Pnode) and isinstance(node2, Pnode):
        x = abs(node1.coordinate[0] - node2.coordinate[0])
        y = abs(node1.coordinate[1] - node2.coordinate[1])
        dist = x + y
        return dist
    else : 
        return None

def get_coordinate(node):     
    if isinstance(node, Pnode):
        return node.coordinate
    else :
        return None
def get_dimension_diff(Xnode1, Xnode2): 
    dimensions1 = get_dimension(Xnode1)
    dimensions2 = get_dimension(Xnode2)
    if dimensions1 == (1,1) or dimensions1 == None:
        return None                         
    if dimensions2 == (1,1) or dimensions2 == None:
        return None     
    try :
        width_diff = dimensions2[1] - dimensions1[0]
        height_diff = dimensions1[1] - dimensions2[0]
        return (width_diff, height_diff)
    except :
        return None

def get_color_difference_set(Xnode1, Xnode2): 
    if isinstance(Xnode1, Vnode) or isinstance(Xnode2, Vnode):
        return None
    colors1 = Xnode1.color
    colors2 = Xnode2.color
    if isinstance(colors1, int):
        return None                          
    if isinstance(colors2, int):
        return None     
    color_diff = [(colors1 - colors2), (colors2 - colors1)]
    return color_diff

def get_component(onode):                   
    return onode.Pnode_list

##def get_bounding_box(Pnode_list, Onode)


##G-node layer DSLs #######################################################
def get_dominant_color(i_value):  
    color_counts = {}
    if isinstance(i_value, Gnode) or isinstance(i_value, Onode):   
        node_list = i_value.Pnode_list
    elif isinstance(i_value, Pnode) or isinstance(i_value, Vnode):
        return None
    else :
        node_list = i_value   
    for node in node_list: color_counts[node.color] = color_counts.get(node.color, 0) + 1
    return max(color_counts, key=color_counts.get)  

def get_background_color_removed(i_value):
    if isinstance(i_value, Gnode):
        pnode_list = i_value.Pnode_list
        node_list = Gnode.node_list
    else :
        node_list = i_value
        pnode_list = []
        for n in i_value:
            if isinstance(n, Pnode):
                pnode_list.append(n)
    dominant_color = get_dominant_color(pnode_list)
    return [node for node in node_list if node.color != dominant_color]


def get_least_common_color(Xnode):               
    color_counts = {}
    if isinstance(Xnode, Pnode) or isinstance(Xnode, Vnode):
        return None
    node_list = Xnode.Pnode_list
    for node in node_list:
        color = get_color_of_node(node)  
        color_counts[color] = color_counts.get(color, 0) + 1
    min_count = min(color_counts.values())
    return [color for color, count in color_counts.items() if count == min_count]
def get_width(Xnode):
    if isinstance(Xnode, Pnode) or isinstance(Xnode, Vnode):
        return None
    "DSL for getting the width of a node-list"
    # print(Xnode)
    # print(Xnode.Pnode_list)
    node_list = Xnode.Pnode_list
    max_v = max(node.coordinate[0] for node in node_list)
    min_v = min(node.coordinate[0] for node in node_list)
    return max_v - min_v + 1
def get_height(Xnode):              
    "DSL for getting the height of a node-list"
    if isinstance(Xnode, Pnode) or isinstance(Xnode, Vnode):
        return None
    node_list = Xnode.Pnode_list
    max_v = max(node.coordinate[1] for node in node_list)
    min_v = min(node.coordinate[1] for node in node_list)
    return max_v - min_v + 1
def get_dimension(Xnode):           
    if isinstance(Xnode, Pnode):
        return (1,1)
    if isinstance(Xnode, Vnode):
        return None
    node_list = Xnode.Pnode_list
    width = get_width(Xnode)
    height = get_height(Xnode)
    return (width, height)
def get_number_of_nodes(Xnode):      
    if isinstance(Xnode, Pnode):
        return 1
    elif isinstance(Xnode, Vnode):
        return None  #######################################
    node_list = Xnode.Pnode_list
    return len(node_list)

def get_corner(Xnode):
    if isinstance(Xnode, Pnode) or isinstance(Xnode, Vnode):
        return None
    
    node_list = Xnode.Pnode_list
    min_x = min(node.coordinate[0] for node in node_list)
    max_x = max(node.coordinate[0] for node in node_list)
    min_y = min(node.coordinate[1] for node in node_list)
    max_y = max(node.coordinate[1] for node in node_list)

    # Determine the corner nodes based on the bounding box
    corners = {(min_x, min_y), (min_x, max_y), (max_x, min_y), (max_x, max_y)}
    return [node for node in node_list if tuple(node.coordinate) in corners]



######################################################################
def get_non_margin(Xnode):                
    if isinstance(Xnode, Pnode) or isinstance(Xnode, Vnode):
        return None
    margin_nodes = []
    node_list = Xnode.Pnode_list
    width = get_width(Xnode)
    height = get_height(Xnode)
    for node in node_list:
        x, y = get_coordinate(node)
        if x == 0 or y == 0 or x == width - 1 or y == height - 1:
            margin_nodes.append(node)
    return margin_nodes




def get_center_nodess(Xnode):      
    if isinstance(Xnode, Pnode):
        # For a single Pnode, it is its own center node
        return [Xnode]
    elif isinstance(Xnode, Onode):
        # For an Onode, return the center Pnodes in its Pnode list
        center_nodes = []
        width = get_width(Xnode)
        height = get_height(Xnode)
        center_x = width // 2 if width % 2 == 0 else width // 2 + 1
        center_y = height // 2 if height % 2 == 0 else height // 2 + 1
        for node in Xnode.Pnode_list:
            if node.coordinate == [center_x, center_y]:
                center_nodes.append(node)
        if len(center_nodes) != 0:
            return center_nodes
        else :
            return None
    elif isinstance(Xnode, Gnode):
        # For a Gnode, return the center Pnodes from its Pnode list
        center_nodes = []
        width = get_width(Xnode)
        height = get_height(Xnode)
        center_x = width // 2 if width % 2 == 0 else width // 2 + 1
        center_y = height // 2 if height % 2 == 0 else height // 2 + 1
        for node in Xnode.Pnode_list:
            if node.coordinate == [center_x, center_y]:
                center_nodes.append(node)
        return center_nodes
    else:
        return None
def get_specific(Gnode, target_colors): 
    node_list = Gnode.Pnode_list
    return [node for node in node_list if node.color in target_colors]

def get_height_difference(Xnode1, Xnode2):  
    height1 = get_height(Xnode1) 
    height2 = get_height(Xnode2)
    if height1 == None or height2 == None:
        return None
    return abs(height1 - height2)

def get_width_difference(Xnode1, Xnode2):  
    width1 = get_width(Xnode1)
    width2 = get_width(Xnode2)
    if width1 == None or width2 == None:
        return None
    return abs(width1 - width2)

def get_max_height(Xnode1, Xnode2):      
    return max(get_height(Xnode1), get_height(Xnode2))    

def get_max_width(Xnode1, Xnode2):
    return max(get_width(Xnode1), get_width(Xnode2))   


###########################################################################
def get_bounding_boxx(onode):
    if not isinstance(onode, Onode):
        return None
    min_x = min_y = float('inf')
    max_x = max_y = float('-inf')
    for pnode in onode.Pnode_list:
        x, y = pnode.coordinate
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)
    return min_x, min_y, max_x, max_y

def get_margin(onode):
    if not isinstance(onode, Onode):
        return None
    margin_nodes = []
    min_x, min_y, max_x, max_y = get_bounding_boxx(onode)
    for pnode in onode.Pnode_list:
        x, y = pnode.coordinate
        if x == min_x or x == max_x or y == min_y or y == max_y:
            margin_nodes.append(pnode)
    return margin_nodes
    
def equal_margin(onode):
    if not isinstance(onode, Onode):
        return None
    equal_margin_onodes = []
    for onode in onode:
        margin_nodes = get_margin(onode)
        if len(margin_nodes) == len(onode.Pnode_list) and \
                all(pnode.color == onode.Pnode_list[0].color for pnode in onode.Pnode_list) and \
                len(onode.Pnode_list) > 7:
            equal_margin_onodes.append(onode)
    return equal_margin_onodes

def is_ring(onode):
    if not isinstance(onode, Onode):
        return False
    margin_nodes = get_margin(onode)
    return len(margin_nodes) == len(onode.Pnode_list) and \
           all(pnode.color == onode.Pnode_list[0].color for pnode in onode.Pnode_list) and \
           len(onode.Pnode_list) > 7

def is_rectangle(onode):
    if not isinstance(onode, Onode):
        return False
    margin_nodes = get_margin(onode)
    if len(margin_nodes) != 4:
        return False
    x_values = [pnode.coordinate[0] for pnode in margin_nodes]
    y_values = [pnode.coordinate[1] for pnode in margin_nodes]
    # Check if the x coordinates form a rectangle
    if len(set(x_values)) != 2:
        return False
    # Check if the y coordinates form a rectangle
    if len(set(y_values)) != 2:
        return False
    return True

def is_square(onode):
    if not isinstance(onode, Onode):
        return False
    # Get the bounding box coordinates
    min_x, min_y, max_x, max_y = get_bounding_boxx(onode)
    # Calculate the width and height of the bounding box
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    # Check if all sides are equal in length and if it's at least 2 by 2
    return width == height and width >= 2

def get_cross_properties(onode):
    if not isinstance(onode, Onode):
        return None
    min_x, min_y, max_x, max_y = get_bounding_boxx(onode)
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    mid_x = (min_x + max_x) // 2
    mid_y = (min_y + max_y) // 2
    return width, height, mid_x, mid_y

def is_cross(onode):
    if not isinstance(onode, Onode):
        return False
    width, height, mid_x, mid_y = get_cross_properties(onode)
    if width <= 2 or height <= 2:
        return False
    has_horizontal_line = False
    has_vertical_line = False
    for pnode in onode.Pnode_list:
        x, y = pnode.coordinate
        if y == mid_y:
            has_horizontal_line = True
        if x == mid_x:
            has_vertical_line = True
    return has_horizontal_line and has_vertical_line

def is_symmetric(onode):
    if not isinstance(onode, Onode):
        return False
    width, height, mid_x, mid_y = get_cross_properties(onode)
    # Check if the Onode is symmetric along both the horizontal and vertical axes
    for pnode in onode.Pnode_list:
        x, y = get_coordinate(pnode)
        if (x != mid_x and y != mid_y) or (x == mid_x and y == mid_y):
            return False  # If any node doesn't have its symmetric counterpart, return False
    
    return True  

def is_contained(onode):##not working will fix it  ????????????????
    nodes = onode.Pnode_list
    filtered_onodes = [node for node in nodes if isinstance(node, Onode)]
    for node in nodes:
        for other_onode in nodes:
            if other_onode is not onode and isinstance(other_onode, Onode):
                other_nodes = other_onode.Pnode_list
                if all(other_node in nodes for other_node in other_nodes):
                    return True
    return False

#############################################################################




###P-O Layer DSL
