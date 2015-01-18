row = [1]
for _ in range(int(input())):
	print(row)
	row = [a + b for a, b in zip([0] + row, row + [0])]
    