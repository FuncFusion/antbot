import requests

vserions_req = requests.get("https://raw.githubusercontent.com/misode/mcmeta/summary/versions/data.json",timeout=10)
versions_original = vserions_req.json()
versions = {ver["id"]: {
	"type": ver["type"],
	"data_pack": ver["data_pack_version"],
	"resource_pack": ver["resource_pack_version"]} for ver in versions_original}

versions["latest"] = {
	"type": versions_original[0]["type"],
	"data_pack": versions_original[0]["data_pack_version"],
	"resource_pack": versions_original[0]["resource_pack_version"]}

def get_mcmeta_ver(pack="data_pack", requested_version="latest"):
	if requested_version == "latest":
		return versions["latest"]
	else:
		try:
			return versions[requested_version][pack]
		except:
			return None

