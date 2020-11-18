"""
Grab bag of utilities
"""

# Merge two dictionaries recursively, copied from Stackoverflow
def merge_dict(d1, d2):
    for k in d2:
        if k in d1 and isinstance(d1[k], dict) and isinstance(d2[k], dict):
            merge_dict(d1[k], d2[k])
        else:
            d1[k] = d2[k]
