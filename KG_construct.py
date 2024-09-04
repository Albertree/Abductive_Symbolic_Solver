from KG_basics import *

dsl_player_only = [get_horizontal_index, get_vertical_index, get_polar_distance, get_manhattan_dist]
dsl_general = [get_coordinate, get_dimension_diff, get_color_difference_set, get_dominant_color,
               get_least_common_color, get_width, get_height, get_dimension, get_number_of_nodes,
               get_corner, get_center_nodess, get_height_difference, get_width_difference]
is_dsl = [is_ring, is_rectangle, is_square, is_symmetric]
is_dsl_question = [is_cross, is_contained]
other_funtion = [get_background_color_removed, get_specific, get_max_height, get_max_width]
isuue_function = [get_margin, get_non_margin, get_color_of_node]

def Make_test_KG(task):
    test_grid = task['test'][0]["input"]
    node_list = Make_NodeList(test_grid)
    edge_list = create_edge_list()

    for dsl in dsl_player_only:
        temp_edge_list = Make_edge_list(node_list, dsl)
        edge_list = Concat_edge_list(temp_edge_list, edge_list)

        temp_edge_list = Make_edge_list(node_list, dsl)
        edge_list = Concat_edge_list(temp_edge_list, edge_list)
        
    temp_node_list, edge_list = Make_Onode(node_list, True, get_polar_distance, edge_list)
    concat_list = Concat_node_list(node_list, temp_node_list)
    temp_node_list, edge_list = Make_Onode(node_list, False, get_polar_distance, edge_list)
    concat_list = Concat_node_list(concat_list, temp_node_list)

    temp_node_list, edge_list = Make_Onode(node_list, True, get_manhattan_dist, edge_list)
    concat_list = Concat_node_list(concat_list, temp_node_list)
    temp_node_list, edge_list = Make_Onode(node_list, False, get_manhattan_dist, edge_list)
    concat_list = Concat_node_list(concat_list, temp_node_list)

    temp_node_list, edge_list = Make_Onode(node_list, True, None, edge_list)
    concat_list = Concat_node_list(concat_list, temp_node_list)
    temp_node_list, edge_list = Make_Onode(node_list, False, None, edge_list)
    concat_list = Concat_node_list(concat_list, temp_node_list)

    node_list = concat_list
    # for n in input_node_list:
    #     print(n)


    node_list, edge_list = Make_Gnode(node_list, edge_list)
    node_list_numbering(node_list, 0)

    wo_background_nodelist = get_background_color_removed(node_list) 

    ## is_same_color should not draw edge between background color Pnodes
    temp_edge_list = Make_edge_list(wo_background_nodelist, get_color_of_node)

    edge_list = Concat_edge_list(temp_edge_list, edge_list)

    for dsl in dsl_general + is_dsl:
        temp_edge_list = Make_edge_list(node_list, dsl)
        edge_list = Concat_edge_list(temp_edge_list, edge_list)
        
    return [node_list, edge_list]

def Make_KG(task):
    num_pairs = len(task["train"])
    input_grids = []
    output_grids = []
    for grid in task["train"]:
        input_grids.append(grid["input"])
    for grid in task["train"]:
        output_grids.append(grid["output"])
        

    KGs = []
    for i in range(num_pairs):
        print("converting task to knowledge graph...", i + 1, "/", num_pairs)
        input_node_list = Make_NodeList(input_grids[i])
        input_edge_list = create_edge_list()
        
        output_node_list = Make_NodeList(output_grids[i])
        output_edge_list = create_edge_list()

        for dsl in dsl_player_only:
            temp_edge_list = Make_edge_list(input_node_list, dsl)
            input_edge_list = Concat_edge_list(temp_edge_list, input_edge_list)

            temp_edge_list = Make_edge_list(output_node_list, dsl)
            output_edge_list = Concat_edge_list(temp_edge_list, output_edge_list)

        ## modify here to add more various type of Onode
        temp_node_list, input_edge_list = Make_Onode(input_node_list, True, get_polar_distance, input_edge_list)
        concat_list = Concat_node_list(input_node_list, temp_node_list)
        temp_node_list, input_edge_list = Make_Onode(input_node_list, False, get_polar_distance, input_edge_list)
        concat_list = Concat_node_list(concat_list, temp_node_list)

        temp_node_list, input_edge_list = Make_Onode(input_node_list, True, get_manhattan_dist, input_edge_list)
        concat_list = Concat_node_list(concat_list, temp_node_list)
        temp_node_list, input_edge_list = Make_Onode(input_node_list, False, get_manhattan_dist, input_edge_list)
        concat_list = Concat_node_list(concat_list, temp_node_list)

        temp_node_list, input_edge_list = Make_Onode(input_node_list, True, None, input_edge_list)
        concat_list = Concat_node_list(concat_list, temp_node_list)
        temp_node_list, input_edge_list = Make_Onode(input_node_list, False, None, input_edge_list)
        concat_list = Concat_node_list(concat_list, temp_node_list)

        input_node_list = concat_list
        # for n in input_node_list:
        #     print(n)


        input_node_list, input_edge_list = Make_Gnode(input_node_list, input_edge_list)

        ## modify here to add more various type of Onode
        temp_node_list, output_edge_list = Make_Onode(output_node_list, True, get_polar_distance, output_edge_list)
        output_node_list = Concat_node_list(output_node_list, temp_node_list)
        output_node_list, output_edge_list = Make_Gnode(output_node_list, output_edge_list)

        node_list_numbering(input_node_list, 0)
        node_list_numbering(output_node_list, 1)

        pair_node_list = Concat_node_list(input_node_list, output_node_list)
        pair_edge_list = Concat_edge_list(input_edge_list, output_edge_list)
        pair_node_list, pair_edge_list = Make_Vnode(pair_node_list, pair_edge_list)

        wo_background_nodelist = get_background_color_removed(pair_node_list) 

        ## is_same_color should not draw edge between background color Pnodes
        temp_edge_list = Make_edge_list(wo_background_nodelist, get_color_of_node)

        pair_edge_list = Concat_edge_list(temp_edge_list, pair_edge_list)
        #print(get_color_of_node.__name__)

        num_dsl = len(dsl_general + is_dsl)
        for i, dsl in enumerate(dsl_general + is_dsl) :
            # print(dsl.__name__)
            progress = (i + 1) / num_dsl * 100
            bar_width = int(progress)
            print('\r [%-*s] %.1f%%' % (100, '=' * bar_width, progress), end='')

            temp_edge_list = Make_edge_list(pair_node_list, dsl)
            pair_edge_list = Concat_edge_list(temp_edge_list, pair_edge_list)




        KGs.append([pair_node_list, pair_edge_list])
        print()
    print('\r ')
    return KGs



def print_adj(kg):
    node_list1 = kg[0]
    edge_list1 = kg[1]
    result1 = [[[0] for i in range(len(node_list1))] for j in range(len(node_list1))]
    for i, edge in enumerate(edge_list1):
        n1, n2 = edge.node_set
        i1 = node_list1.index(n1)
        i2 = node_list1.index(n2)
        result1[i1][i2][0] += 1
        result1[i1][i2].append(edge.tag)
    count_edge1 = None
    return result1, count_edge1
