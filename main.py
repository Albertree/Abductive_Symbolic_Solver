from KG_basics import *
from KG_construct import *
from Solver import *
from Specifier import *
from Solution_generator import *

import os
import json
from pathlib import Path

correct_list_c = []
wrong_list_c = []

files = os.listdir("./data/training/")
index = 0
# Loop through each file
for index, f in enumerate(files):
    file_path = "./data/training/" + f  
    try:
        with open(file_path) as file:
            task = json.load(file)
            
        print(f"Processing file: {f} ({index + 1}/{len(files)})")

        # Extract truth color set
        truth_color_set = {color for row in task["test"][0]["output"] for color in row}

        # Call function to predict color sets
        candi_answer_h, candi_answer_w, candi_answer_color_sets = GridSize_pridictorr(task)
        
        print(f"Found {len(candi_answer_color_sets)} color set answers")
        print(f"Truth Color Set: {truth_color_set}")
        print("Predicted Color Sets:")
        for color_set in candi_answer_color_sets:
            print(color_set)
        
        # Check if any predicted color set matches truth
        color_correct = any(color_set == truth_color_set for color_set in candi_answer_color_sets)
        if color_correct:
            print("Color Set Correct!")
            correct_list_c.append(f)
        else:
            print("Color Set Incorrect!")
            wrong_list_c.append(f)
        
    except Exception as e:
        print(f"Error processing file: {f}")
        print(e)

# Print results
print(f"Correct: {len(correct_list_c)}, Wrong: {len(wrong_list_c)}")


