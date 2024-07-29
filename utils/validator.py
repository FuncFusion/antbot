from Levenshtein import distance

def validate(string, valid_strings):
	string = string.lower()
	for valid_string in valid_strings:
		if distance(string, valid_string) <= len(valid_string)/2:
			return valid_string
		else:
			for alias in valid_strings[valid_string]:
				alias = alias.lower()
				if distance(string, alias) <= len(alias)/2:
					return valid_string
	return None

def all_valid(string, valid_strings):
	matched_strings = []
	for valid_string in valid_strings:
		for alias in valid_strings[valid_string]:
			if string.lower() in alias.lower() or distance(string, alias) <= len(alias)/2:
				matched_strings.append(valid_string)
				break
	return matched_strings