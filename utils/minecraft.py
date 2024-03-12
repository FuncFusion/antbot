import requests
from collections import OrderedDict as odict

from Levenshtein import distance
from bs4 import BeautifulSoup

def get_mcmeta_ver(type="dp", version="latest"):
	versions = odict()
	# Set up
	pf_req = requests.get("https://minecraft.wiki/w/Pack_format",timeout=10)
	pf_content = BeautifulSoup(pf_req.content, "html.parser")
	table, title, desc = None, "", ""
	if type == "dp":
		table = pf_content.find_all("table")[1]
	else:
		table = pf_content.find("tbody")
	#
	for row in table.find_all("tr"):
			cells = row.find_all("td")
			if len(cells) >= 2:
				num = cells[0].get_text()
				snapshot = cells[1].get_text()
				release = cells[2].get_text()
				for rel in release.split("–"):
					versions.update({rel: num})
				versions.update({snapshot: num})
	if version == "latest":
		return int(list(versions.items())[0][1])
	else:
		for ver in versions:
			if distance(version, ver) <= len(ver)/4:
				return versions[ver]
		else:
			return int(list(versions.items())[0][1])

