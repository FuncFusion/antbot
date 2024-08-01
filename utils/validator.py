from Levenshtein import distance

def validate(string, valid_strings, accuracy=2):
	string = string.lower()
	for valid_string in valid_strings:
		if distance(string, valid_string) <= len(valid_string)/accuracy:
			return valid_string
		else:
			for alias in valid_strings[valid_string]:
				alias = alias.lower()
				if distance(string, alias) <= len(alias)/accuracy:
					return valid_string
	return None

def all_valid(string, valid_strings, accuracy=2):
	matched_strings = []
	string = string.lower()
	for valid_string in valid_strings:
		if string in valid_string.lower() or distance(string, valid_string) <= len(valid_string)/accuracy:
			matched_strings.append(valid_string)
		else:
			for alias in valid_strings[valid_string]:
				if string in alias.lower() or distance(string, alias) <= len(alias)/accuracy:
					matched_strings.append(valid_string)
					break
	return matched_strings