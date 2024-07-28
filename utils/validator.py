from Levenshtein import distance

def validate(string, valid_strings):
	for valid_string in valid_strings:
		if distance(string, valid_string) <= len(valid_string)/2:
			return valid_string
		else:
			for alias in valid_strings[valid_string]:
				if distance(string, alias) <= len(alias)/2:
					return valid_string
	return None

def least_distance(string, valid_strings):
	for valid_string in valid_strings:
		distances = (distance(string, alias) for alias in valid_strings[valid_string])
	return min(distances)