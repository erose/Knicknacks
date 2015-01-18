def string_to_int(s):
	count = 0
	for i, char in enumerate(s):
		if char == "-":
			return count + 10 * string_to_int(s[count+1:])
		elif char == "*":
			count += 1
	return count

if __name__ == "__main__":
	string = input()
	string = "".join(reversed(string))
	print(string_to_int(string))