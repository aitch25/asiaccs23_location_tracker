import editdistance
def jaccard(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union

print(editdistance.eval(['Jeongja', 'Pangyo', 'Cheonggyesan', 'Migeum', 'Dongcheon', 'Suji-gu Office', 'Jeongja'], ['Sanghyeon', 'Seongbok', 'Suji-gu Office', 'Dongcheon', 'Migeum', 'Jeongja', 'Pangyo']))
print(jaccard(['Jeongja', 'Pangyo', 'Cheonggyesan', 'Migeum', 'Dongcheon', 'Suji-gu Office', 'Jeongja'], ['Sanghyeon', 'Seongbok', 'Suji-gu Office', 'Dongcheon', 'Migeum', 'Jeongja', 'Pangyo']))
print(jaccard(['A', 'B', 'C', 'D', 'E'], ['B', 'C', 'D', 'E', 'F']))
print('5', jaccard(['A', 'B', 'C', 'D', 'E'], ['C', 'D', 'E', 'F', 'G']))
print('6', jaccard(['A', 'B', 'C', 'D', 'E', 'F'], ['C', 'D', 'E', 'F', 'G', 'H']))
print('7', jaccard(['A', 'B', 'C', 'D', 'E', 'F', 'H'], ['C', 'D', 'E', 'F', 'G', 'H', 'I']))
print('7', jaccard(['A', 'B', 'C', 'D', 'E', 'F', 'H'], ['D', 'E', 'F', 'G', 'H', 'I', 'J']))

