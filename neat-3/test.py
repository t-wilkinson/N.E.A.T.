


'''
find connections sharing same node
'''
# l = [[0, 1], [4, 5], [6, 8], [3, 2], [4, 7]]
# def find(num1, num2, l):
# 	l = [frozenset(x) for x in l]
# 	d = {num1: set(), num2: set()}

# 	for s in l:
# 		inter = {num1, num2} & s
# 		if inter:
# 			(inter_val,) = inter
# 			d[inter_val] = s ^ inter
# 	return d[num1] & d[num2] or 'hi'
			
# num = find(5, 7, l)
# print(num)



'''
flatten list
'''
# def flatten(l, ltypes=(list, tuple)):
# 	ltype = type(l)
# 	l = list(l)
# 	for i in range(len(l)):
# 		while isinstance(l[i], ltypes):
# 			if not l[i]:
# 				l.pop(i)
# 				i -= 1
# 				break
# 			else:
# 				l[i:i + 1] = l[i]
# 	return ltype(l)

# a = []
# for i in range(20, 0, -1):
# 	a = [a, i]
# a = flatten(a)
# # print(a)



'''
group values if they are equal
'''
# next_dict = {}
# cur_nums = [1, 4, 3, 5, 9, 2, 4, 4]

# for num in cur_nums:
# 	for i, next_list in next_dict.items():
# 		if num == next_list[0]:
# 			next_dict[i].append(num)
# 			break
# 	else:
# 		next_dict[len(next_dict)] = [num]

# print(next_dict)



'''
simulate feed through in neural network
'''
# connections = [[0, 2], [1, 2], [0, 3], [1, 3], [0, 4], [1, 4], [2, 5], [3, 5], [4, 5]]
# inputs = tuple((0, 1))
# outputs = tuple((5,))
# layers = {inputs: []}

# def find_layers(connections):
# 	for i, c in enumerate(connections):
# 		for prev_layer, layer in layers.items():
# 			if c[0] in prev_layer:
# 				if c[1] not in layer:
# 					layer.append(c[1])
# 					connections.pop(i)
# 					break
# 		else:
# 			if layers[prev_layer][0] in outputs:
# 				break
# 			next_layer = tuple(layers[prev_layer])
# 			layers[next_layer] = [c[1]]

# find_layers(connections)
# print(layers)


