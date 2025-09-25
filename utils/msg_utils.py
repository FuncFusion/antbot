from utils.shortcuts import no_ping
from re import split, DOTALL

async def get_msg_by_id_arg(self, ctx, bot, arg:str):
	try:
		id = (arg.split("/")[-2:])
		if len(id) == 2 or (len(id:=id[0].split("-")) == 2): 
			chnl = bot.get_channel(int(id[0]))
			msg = await chnl.fetch_message(int(id[1]))
		else:
			msg = await ctx.channel.fetch_message(int(id[-1]))
		return msg
	except Exception as e:
		return e


def split_msg(s):
	MAX_LENGTH = 2000
	blocks = split(r'(```.*?```)', s, flags=DOTALL)
	parts = []
	current_part = ''
	for block in blocks:
		if block.startswith('```'):  # This is a block of code
			lines = block.split('\n')
			for line in lines:
				if len(current_part) + len(line) + 1 > MAX_LENGTH:  # Adding this line would exceed the limit
					# Close the current part and start a new one
					current_part += '```\n'
					parts.append(current_part)
					current_part = '```ansi\n' + line
				else:
					current_part += line + '\n'
		else:  # This is normal text
			separator = "\n" if s.count(" ") < s.count("\n") else " "
			words = block.split(separator)
			for word in words:
				if len(current_part) + len(word) + 1 > MAX_LENGTH:  # Adding this word would exceed the limit
					# Start a new part
					parts.append(current_part)
					current_part = word + separator
				else:
					current_part += word + separator
	if current_part != '':
		parts.append(current_part)

	for i in range(parts.count('')):
		parts.remove('')
	return parts

def user_from_embed(message):
	return int(message.embeds[0].author.icon_url.split("/")[4])

class Emojis:

	ajmeta = "<:ajmeta:1319409157648154738>"
	mcf = "<:mcfunction:1142345406106312754>"
	mcf_tick = "<:mcfunction_tick:1142345408459321425>"
	mcf_load = "<:mcfunction_load:1142345404403425341>"
	json = "<:json:1142345204402233434>"
	nbt = "<:nbt:1142345418949279753>"
	bbmodel = "<:bbmodel:1186764426376904714>"
	lang_file = "<:lang_file:1188838193559257258>"


	folder = "<:folder:1142345186949734482>"
	folder_open = "<:folder_open:1142345194805669918>"        
	assets = "<:assets:1142346878030184518>"
	assets_open = "<:assets_open:1142346941599064086>"
	data = "<:data:1142345181564260413>"
	data_open = "<:data_open:1142345183367802971>"
	namespace = "<:namespace:1188839155170545705>"
	namespace_open = "<:namespace_open:1188839157829742723>"
	tick_json = "<:tickjson:1188838117940133930>"
	load_json = "<:loadjson:1188838120712577174>"
	sounds_json = "<:sounds_json:1142347091759353866>"
	pack_mcmeta = "<:pack_mcmeta:1142345410380304414>"


	advancement = "<:advancements:1142345174580740096>"
	banner_pattern = "<:banner_pattern:1246812883170492436>"
	chat_type = "<:chat_type:1142345176921145435>"
	damage_type = "<:damage_type:1142345178766659614>"
	dimension = "<:dimension:1142928197168668752>"     
	dimension_type = "<:dimension_type:1143112349214068796>"
	enchantment = "<:enchantment:1246812751938977915>"
	function = "<:functions:1142345196642775090>"     
	item_modifier = "<:item_modifiers:1142345199700414564>"
	instrument = "<:instrument:1319409530974638100>"
	loot_table = "<:loot_tables:1142345293170491472>"
	painting_variant = "<:painting_variant:1246812947083432026>"
	predicate = "<:predicates:1142345430139666524>"
	recipe = "<:recipes:1188841592715489361>"
	structure = "<:structures:1142345436942827550>"
	tags = "<:tags:1319409235171344454>"
	trial_spawner = "<:trial_spawner:1319409245610971276>"
	trim_material = "<:trim_material:1319409249264341013>"
	trim_pattern = "<:trim_pattern:1319409547101605969>"
	worldgen = "<:worldgen:1142345441523019796>"
	wolf_variant = "<:wolf_variant:1246817007161180232>"

	atlases = "<:atlases:1142347325436612619>"
	blockstates = "<:blockstates:1142346756953231451>"
	equipment = "<:equipment:1319409526704832553>"
	font = "<:font:1142346540392927262>"
	items = "<:items:1319409532858007563>"
	lang = "<:lang:1142346828206047325>"
	models = "<:models:1142346673469800479>"
	particles = "<:particles:1142346351879925862>"
	post_effect = "<:shaders:1142346604028899429>"
	sounds = "<:sounds:1142347049568837742>"
	shaders = "<:shaders:1142346604028899429>"
	texts = "<:texts:1142919111236665485>"
	textures = "<:textures:1142347361893494876>"


	advancement_file = "<:advancement:1319409155756527716>"
	banner_pattern_file = "<:banner_pattern:1246812899192737862>"
	chat_type_file = "<:chat_type_file:1188838139700195348>"
	damage_type_file = "<:damage_type_file:1188838136957112420>"
	dimension_file = "<:dimension_file:1188838135300366336>"
	dimension_type_file = "<:dimension_type_file:1188838133857534002>"
	enchantment_file = "<:enchantment:1246812661866561536>"
	item_modifier_file = "<:item_modifier:1188838125565382728>"
	instrument_file = "<:instrument_file:1319409210257182831>"
	loot_table_file = "<:loot_table_file:1319409534510432388>"
	painting_variant_file = "<:painting:1142345422233423942>"
	predicate_file = "<:predicate:1188838122633576488>"
	recipe_file = "<:recipe:1188838131299004466>"
	tags_file = "<:tags_file:1319409237830406154>"
	trial_spawner_file = "<:trial_spawner_file:1319409581360939150>"
	trim_material_file = "<:trim_material_file:1319409251386527766>"
	trim_pattern_file = "<:trim_pattern_file:1319409255337427105>"
	wolf_variant_file = "<:wolf:1246816990669312011>"
	worldgen_file = "<:worldgen_file:1319409262602223658>"

	atlases_file = "<:atlas:1188838144351682620>"
	blockstates_file = "<:blockstate:1188838141663125624>"
	equipment_file = "<:equipment_file:1319409197108170752>"
	items_file = "<:items_file:1319409214614929478>"
	particles_file = "<:particle:1188838146385911939>"
	post_effect_file = "<:shader_triangle:1285663956496810048>"


	beet = "<:beet:1143125070336774165>"
	bolt = "<:bolt:1142918894571491429>"
	dot_vscode = "<:dot_vscode:1186764449441402890>"
	vscodeignore = "<:vscodeignore:1186765769149775903>"
	datapacks_open = "<:datapacks:1186764442277527713>"
	assembly = "<:assembly:1186764422312632411>"
	src = "<:src:1186764511538061422>"
	src_open = "<:src_open:1201954005928910888>"
	no_dp_icons = "<:no_dp_icons:1194373013064405054>"
	deta_rack = "<:deta_rack:1273708974839038123>"
	resource_rack = "<:resource_rack:1273708997048012951>"
	program_rack = "<:programrack:1191038718329495642>"
	sparkles = "<:sparkles_be:1145692031625220216>"
	pack_mcmeta2 = "<:packmcmeta2:1188841036898914335>"
	bot = "<:bot:1208116530643210281>"
	calendar = "<:calendar:1208149889591021649>"
	check = "<:check:1208116534078079037>"
	cross = "<:cross:1208116535546355733>"
	crown = "<:crown:1208116537295118396>"
	deleted_msg = "<:deleted_msg:1208148592519417896>"
	edited_msg = "<:edited_msg:1208116541082566748>"
	exclamation_mark = "<:exclamation_mark:1208116542877999164>"
	id = "<:id:1208116544362512384>"
	link = "<:link:1208166246886019112>"
	question_mark = "<:question_mark:1208116636528156742>"
	role = "<:role:1208116549198811166>"
	speaker = "<:speaker:1208116723534798898>"
	spyglass = "<:spyglass:1208148591269519370>"
	text_channel = "<:text_channel:1208116557126041640>"
	user = "<:user:1208116558350516255>"
	users = "<:users:1208116665825497129>"
	pin = "<:pushpin:1270665261120356454>"
	door = "<:door:1232042414613594112>"
	mute = "<:mute:1232042437178949754>"
	ban = "<:ban:1232045190739525652>"
	bell = "<:bell:1250909629165342842>"
	party_popper = "<:party_popper:1255829653965242449>"
	trophy = "<:trophy:1256921258797437020>"
	vc_left = "<:vc_left:1268653354477813862>"
	vc_joined = "<:vc_joined:1268653332860502056>"
	anchor = "<:anchor:1274090060320604200>"
	blocks = "<:blocks:1274090523086295122>"
	blocks2 = "<:blocks2:1274090539968499752>"
	bossbar = "<:bossbar:1274090597812273162>"
	antvote = "<:antvote:1042075029040545922>"
	packformat = "<:packformat:1277533907620991026>"
	downtvote = "<:downtvote:1042076436363751434>"
	dice = "<:dice:1277384663836528682>"
	missing = "<:missing:1278053472117194814>"
	typing = "<a:typing:1284598739025268910>"
	shader_triangle = "<:shader_triangle:1285663956496810048>"
	bth123 = "<:bth123:1321085135541768324>"
	superant_ = "<:ant:1321085150167040000>"
	amandin = "<:amandin:1321085166168571987>"

	boolean = "<:boolean:1274090578703028298>"
	byte = "<:byte:1274090632230600704>"
	compound = "<:compound:1274090641462399007>"
	data_storage = "<:data_storage:1274090653189541919>"
	double = "<:double:1274090664325546077>"
	effect = "<:effect:1274090670306492436>"
	entity_type = "<:entity_type:1274090677264842816>"
	float = "<:float:1274090703957528576>"
	int = "<:int:1274090712052273243>"
	item = "<:item:1274090719719456778>"
	list = "<:list:1274090727181123594>"
	long = "<:long:1274090734731006042>"
	pos = "<:pos:1274090741538357261>"
	pos2 = "<:pos2:1274090748240855130>"
	selector = "<:selector:1274090757833101433>"
	selector2 = "<:selector2:1274090765454151804>"
	short = "<:short:1274090772051918858>"
	slot = "<:slot:1274090780624945244>"
	string = "<:string:1274090787205939314>"
	macro = "<:macro:1276929717227880563>"


	github = "<:github:1276178127717924947>"
	svelte = "<:svelte:1259210189282742355>"
	image = "<:painting:1142345422233423942>"
	md = "<:readme_md:1142345432387817534>"
	txt = "<:txt:1142918900166688798>"
	vsh = "<:vsh:1142347174223552543>"
	fsh = "<:fsh:1142347278812725258>"
	glsl = "<:glsl:1142347436740849745>"
	ogg = "<:ogg:1142918898157629620>"
	misc = "<:misc:1142345412938834022>"
	license = "<:license:1246813468108001392>"
	copyright = "<:copyright_txt:1142893165574107146>"
	vsc = "<:vsc:1277217993021194240>"
	blockbench = "<:blockbench:1420003168451825674>"
	python = "<:Python:542498804931362817>"
	pycd = "<:python_compiled:1186764498091135087>"
	pycache = "<:pychache:1186765566808170496>"
	c = "<:c_:1186764428528599090>"
	cpp = "<:cpp:1186764430076301373>"
	cs = "<:cs:1186764433280745593>"
	html = "<:html:1186764467976011918>"
	css = "<:css:1186764434757128254>"
	mojo = "<:mojo:1186764485592096778>"
	js = "<:javascript:1186765428433879110>"
	ts = "<:typescript:1186765725285761214>"
	re = "<:reasonreact:1186764503036211290>"
	java = "<:java:1186765389967925339>"
	r = "<:r_:1186764500247003177>"
	git = "<:git:1186764459872620634>"
	gitignore = "<:gitignore:1186764463433601084>"
	go = "<:golang:1186764465107116234>"
	kotlin = "<:kotlin:1186764479199973466>"
	exe = "<:executable:1186764814358417580>"
	shell = "<:shell:1186765660118843553>"
	android = "<:android:1186764415131992246>"
	xml = "<:xml:1186764525786124369>"
	yaml = "<:yaml:1186764528315277353>"
	archive = "<:archive:1186764416503525406>"
	jar = "<:jar:1419771070205919282>"
	sublime = "<:sublime:1186764513198997614>"
	sublime_package = "<:sublime_package:1186765697834041475>"
	ruby = "<:ruby:1201952259190300742>"
	rust = "<:rust:1186764506605559868>"
	pdf = "<:pdf:1186765519970385980>"
	jmc = "<:jmc:1186764477241245886>"
	hjmc = "<:hjmc:1186765343012704367>"
	log = "<:log:1186764481682997368>"
	database = "<:database:1186764439349887218>"
	php = "<:php:1186764490356834366>"
	lua = "<:lua:1186765470121087047>"
	doc = "<:doc:1186764446316646530>"
	excel = "<:excel:1186764451756650566>"
	ttf = "<:font:1186764454789124147>"
	swift = "<:swift:1186764516810309807>"
	autohotkey = "<:autohotkey:1186764424829210634>"
	arduino = "<:arduino:1186764419208851517>"
	dart = "<:dart:1186764437789626438>"
