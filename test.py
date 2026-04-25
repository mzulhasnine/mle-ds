
from collections import defaultdict  
groups = defaultdict(list)  
print(groups)  
   
groups['A']
print(groups)  
  
# data = [ ("A", 10),  ("A", 20),  ("B", 5) ]  
  
# for key, value in data:  groups[key].append(value)  
  
# # {'A': [10, 20], 'B': [5]}

# Without `defaultdict`, you would write:

# groups = {}  
  
# for key, value in data:  
#     if key not in groups:  
#         groups[key] = []  
#     groups[key].append(value)