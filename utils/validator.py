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

def closest_match(string, valid_dict, distance_limit=0):
	best_match = None
	best_distance = float('inf')
	string = string.lower()
	for key, aliases in valid_dict.items():
		if string == key.lower():
			return key
		for alias in aliases:
			if string == alias.lower():
				return key
		key_distance = distance(string, key)
		if key_distance < best_distance:
			best_match = key
			best_distance = key_distance
		for alias in aliases:
			alias_distance = distance(string, alias)
			if alias_distance < best_distance:
				best_match = key
				best_distance = alias_distance
	if distance_limit > 0 and best_distance > distance_limit:
		return None
	return best_match
