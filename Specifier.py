from KG_basics import *
from KG_construct import *
from Solver import *

#I didnot addd modifications to this extractor function 
def extractor(KG, adj, target_xnode):
    node_info = {}
    node_info["type"] = target_xnode.type
    node_info["properties"] = set()

    if isinstance(target_xnode, Gnode):
        node_info["definition"] = "Gnode"
        return node_info
    else :
        node_info["definition"] = target_xnode.condition

    # edge_list = KG[1]
    edge_dict = {}
    # print("node type : ", type(target_xnode))

    # print("preparing edge list... ")
    # result, _ = print_adj(KG)
    index = KG[0].index(target_xnode)
    for i, n in enumerate(KG[0]):
        if n.output == 1:
            break
    index2 = i
    for edge in adj[index:index2]:
        if edge[0] == 0:
            continue
        # print(edge[1])
        for tag in edge[1:]:
            # print("tag : ", tag)
            edge_dict[tag[0]] = edge[0]
    # print("\rfinish edge list")

    max_size = 0
    min_size = 900
    unique = 1
    for node in KG[0]:
        if node.type == "Onode" and node.condition == target_xnode.condition and node.input == 1:
            if node.color == target_xnode.color and node != target_xnode:
                unique = 0
            max_size = max(max_size, get_number_of_nodes(node))
            min_size = min(max_size, get_number_of_nodes(node))
    if max_size <= get_number_of_nodes(target_xnode):
        node_info["properties"].add("max_size")
    if min_size >= get_number_of_nodes(target_xnode):
        node_info["properties"].add("min_size")
    if unique == 1:
        node_info["properties"].add("unique_color")

    if "is_ring" in edge_dict.keys():
        node_info["properties"].add("ring_shape")
    if "is_rectangle" in edge_dict.keys():
        node_info["properties"].add("rectangle_shape")
    if "is_square" in edge_dict.keys():
        node_info["properties"].add("square_shape")
    if "is_symmetric" in edge_dict.keys():
        node_info["properties"].add("symmetric")

    node_info["edge_list"] = edge_dict
    return node_info




from itertools import combinations
#there is no any modifications done to this specifier function 
def specifer(KG, adj,target_xnode):  ## 다시 짜야할 것 같다. -> 람다함수 말고 그냥 유일하게 가지고 있는 특성들을 리스트로 반환하는 함수
    # adj, _ = print_adj(KG)
    node_info = extractor(KG, adj, target_xnode)
    speic = []
    if node_info["type"] == "Gnode":
        speic.append(("definition", "Gnode"))
        return tuple(speic)
    
    candi_node_list = []
    for n in KG[0]:
        if n.input  == 1 and (n.type == "Onode" or n.type == "Gnode") :
            candi_node_list.append(extractor(KG, adj, n))
    
    obj_def = node_info["definition"]
    speic.append(("definition", obj_def))
    
    for property in node_info["properties"]:
        speic.append(("properties", property))


    all_combinations = []
    for r in range(1, len(speic) + 1):
        all_combinations.extend(combinations(speic, r))

    # print("properties of target_node :", speic)
    for i, combo in enumerate(all_combinations):
        # print("combo :", combo)
        t_node = []
        for candi_info in candi_node_list:
            # print("candi_info :", candi_info)
            match = 1
            for c in combo :
                # print(c[0], c[1])
                if c[0] == "definition":
                    if c[1] != candi_info[c[0]] :   
                        match = 0    
                else :
                    if c[1] not in candi_info[c[0]]:
                        match = 0  
            if match == 1:
                t_node.append(n)
                # print("추가됨")
        # print("len of t_node :", len(t_node))
        if len(t_node) == 1:
            return combo
        else :
            continue
    return None

