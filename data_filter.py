from itertools import permutations
def filtered_permutations(input_dict,first_link = {},depth=4):
    filtered_items = [key for key, value in input_dict.items() if value[0] <= 6]# 筛选出value小于6的元素
    if first_link == []:
        valid_permutations = list(permutations(filtered_items, depth))
    else:
        #print(filtered_items)
        # 进一步筛选出符合first_link条件的元素作为排列的第一位
        first_elements = [key for key in filtered_items if key in first_link]
        #print(first_elements)
        # 筛选出不符合first_link条件的元素作为排列的后续位
        other_elements = [key for key in filtered_items if key not in first_link]

        # 生成所有有效的排列：第一位来自first_elements，后续位来自other_elements或first_elements剩余部分
        valid_permutations = []
        for first in first_elements:
            for perm in permutations(other_elements, depth):
                valid_permutations.append((first,) + perm)
    return valid_permutations