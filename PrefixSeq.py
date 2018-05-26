import copy
from collections import defaultdict

'''
individual transaction sequence: [["a"], ["b"], ["c"]]
transaction DB = [
                [["a"], ["b"], ["c"]],
                [["a"], ["b"], ["c"],["d"]],
                [["a"], ["c"], ["e"]],
                [["b"], ["c"], ["e"]]
                ]
'''

'''
Basically a divide-conquer algorithm is used to complet prefix search on sequential patterns.
1. Find from database all items which have at least support s. Add them to iList.
(Here we have s = 2)
2. Run prefixSearch(Database,iList,s)
def prefixSpan(Database,iList,s)
    for x in iList:
    Form x_projectDB (project Database based x prefix);
    Find supported Items;
    Prune x-project;
    If x-project has more than one sequence:
        nextLewel=prefixSearch(X_projectDB,Items,s);
        IList=join(x,Items+nextLewel);
    Return IList;
'''

'''
Define Function to project Sequence/Database based on given prefix
'''

def projectSequence(sequence, prefix, newEvent):
    '''
    Args:
        sequence: input sequence for projection
        prefix: input prefix for search
        newEvent: first item ignore if True
    Return:
        None if not contain prefix
        a new suffix sequence (corresponding to prefix)
    '''
    projectSeq = None
    for i, item in enumerate(sequence):
        if projectSeq is None:
            if (not newEvent) or (i>0):
                if (all(y in item for y in prefix)):
                    projectSeq = [list(item)]
        else:
            projectSeq.append(copy.copy(item))
    return projectSeq

def projectDatabase(database, prefix, newEvent):
    '''
    Args:
        sequence: input database for projection
        prefix: input prefix for search
        newEvent: first item ignore if True
    Return:
        [] if not contain prefix
        a new suffix database (corresponding to prefix)
    '''
    projectDB = []
    for sequence in database:
        projectSeq = projectSequence(sequence, prefix, newEvent)
        if not projectSeq is None:
            projectDB.append(projectSeq)
    return projectDB

'''
Generate a list of all items that are contained in a database
'''
def getItems(database):
    revtal = set(item for sequence in database for itemset in sequence for item in itemset)
    return revtal
'''
Generate a dict that map each item to its support in database
'''
def getSupports(database, newEvent=False, prefix = []):
    result = defaultdict(int)
    for sequence in database:
        if newEvent:
            sequence = sequence[1:]
        uniqueItems = set()
        for itemset in sequence:
            if all(y in itemset for y in prefix):
                for item in itemset:
                    if not item in prefix:
                        uniqueItems.add(item)
        for item in uniqueItems:
            result[item] +=1
    return sorted(result.items())

'''
Search patterns based on prefix shrinking searching
'''

def prefixSearch(database, min_threshold):
    # return list [(item, support)]
    revtal = []
    itemStat = getSupports(database)
    for item, stats in itemStat:
         if (stats>=min_threshold):
             newPrefix = [[item]]
             revtal.append((newPrefix, stats))
             subVariable = prefixSearchRecursive(projectDatabase(database, [item], False), min_threshold, newPrefix)
             revtal.extend(subVariable)
    return revtal

def prefixSearchRecursive(database, min_threshold, last_prefix):
    revtal = []

    #current prefix projection
    itemStatCurrent = getSupports(database, False, last_prefix)
    for item, stats in itemStatCurrent:
        if (stats >= min_threshold) and item > last_prefix[-1][-1]:
            newPrefix = copy.deepcopy(last_prefix)
            newPrefix[-1].append(item)
            revtal.append((newPrefix, stats))
            subVariable = prefixSearchRecursive(projectDatabase(database, newPrefix[-1], False), min_threshold, newPrefix)
            revtal.extend(subVariable)

    # new event to prefix
    itemStatSub = getSupports(database, True)
    for item, stats in itemStatSub:
        if stats >= min_threshold:
            newPrefix = copy.deepcopy(last_prefix)
            newPrefix.append([item])
            revtal.append((newPrefix, stats))
            subVariable = prefixSearchRecursive(projectDatabase(database, [item], True), min_threshold, newPrefix)
            revtal.extend(subVariable)
    return revtal

if __name__ == "__main__":

    # test case 1:
    database1 = [
        [["a"],["d"]],
        [["a"],["b"],["d"]],
        [["c"],["d"]],
        [["a"],["b"],["c"],["d"]],
        [["b"],["c"]],
        [["d"]],
        [["b"],["c"],["d"]]
    ]
    # higher than 2 , so min_threshold =3
    print("Database1 (support over 3): \n{}".format(prefixSearch(database1, 3)))

    # test case 2
    database2 = [
    [["a"], ["e"]],
    [["a"], ["b"], ["f"]],
    [["c"], ["d"]],
    [["a"], ["b"], ["c"], ["f"]],
    [["b"], ["e"]],
    [["d"]],
    [["b"], ["c"], ["e"]],
    [["a"], ["f"], ["g"]],
    [["b"], ["e"], ["g"]]
    ]

    print("Database 2 (support over 3)\n{}".format(prefixSearch(database2, 3)))
