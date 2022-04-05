import sexpdata
import sys
from sexpdata import Symbol;

rendered_references = sys.argv[1].split(',')

def die(why):
	print(why)
	exit(1)

def get_fp_text(footprint, kind):
	for fp_text in footprint:
		if isinstance(fp_text, list) and fp_text[0] == Symbol('fp_text') and fp_text[1] == Symbol(kind):
			return fp_text[2]

def footprint_donthide(footprint):
	for model in footprint:
		if isinstance(model, list) and model[0] == Symbol('model'):
			try:
				model.remove(Symbol('hide'))
			except ValueError:
				pass

def footprint_hide(footprint):
	footprint_donthide(footprint)
	for model in footprint:
		if isinstance(model, list) and model[0] == Symbol('model'):
			model.append(Symbol('hide'))

data = sexpdata.load(open(sys.argv[2], 'r'))

if data[0] != Symbol("kicad_pcb"):
	print(data[0])
	die("Expected 'kicad_pcb' item at start of file")

for footprint in data:
	if isinstance(footprint, list) and footprint[0] == Symbol('footprint'):
		reference = get_fp_text(footprint, 'reference')
		if reference in rendered_references:
			print("Showing %s" % reference)
			footprint_donthide(footprint)
		else:
			print("Hiding %s" % reference)
			footprint_hide(footprint)

result = sexpdata.dumps(data).replace('*\\.', '*.')
print(result, file=open(sys.argv[3], 'w'))
