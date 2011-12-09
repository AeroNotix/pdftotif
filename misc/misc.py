#-------------------------------Helper Functions--------------------------------

"""
Any function that does not directly interact with classes or data
"""

def cleanup(deletions):

    """
    Deletes temporary files
    """
    for fname in deletions:
        os.remove(fname)

def encase(string, target):
    """
    Encases a string in another string
    """
    return string+target+string