import copy 

def parse(path):
	parameters = {}
	rules = []
	try:
		with open(path,'r') as f:
			lines = f.readlines()
	except:
		print "No se puede abrir el archivo "+path
		return

	for line in lines:
		if not line or line.startswith('-') or line.startswith('#'): continue
		if line.startswith('IF'):
			current = {}
			sides = line.replace('IF','').split('THEN')
			current['LHS'] = {}
			conditions = sides[0].split('&')

			for condition in conditions:
				HS = map(str.strip,condition.split('=',1))
				current['LHS'][HS[0]] = [s.strip() for s in HS[1].split('|')]
			
			action = sides[1]
			HS = map(str.strip,action.split('='))
			current['LHS'] = {HS[0] : HS[1]}
			rules.append(copy.deepcopy(current))

		else:
			splitline = line.split('=',1)
			parameters[splitline[0].strip()] = [s.strip() for s in splitline[1].split('|')]

		return parameters,rules