#!/bin/python

import sexpdata
import sys
from sexpdata import Symbol
import re

def decompose_ref(ref):
	m = re.match("([a-zA-Z]+)([0-9]+)", ref)
	if m is not None:
		return (m[1], int(m[2]))

def parse_filters(ref_filters):
	refs = []
	ref_ranges = []
	for filt in ref_filters:
		m = re.match("([A-Za-z]+)([0-9]+)-([0-9]+)", filt)
		if m is None:
			refs.append(filt)
		else:
			ref_ranges.append((m[1], int(m[2]), int(m[3])))
	return (refs, ref_ranges)

def filter_matches(ref, filters):
	if ref in filters[0]: return True
	decomp = decompose_ref(ref)
	if decomp is not None:
		for r in filters[1]:
			if r[0] == decomp[0] and r[1] <= decomp[1] and decomp[1] <= r[2]:
				return True
	return False

ref_filters = parse_filters(sys.argv[1].split(','))

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
		if filter_matches(reference, ref_filters):
			print("Showing %s" % reference)
			footprint_donthide(footprint)
		else:
			print("Hiding %s" % reference)
			footprint_hide(footprint)

result = sexpdata.dumps(data).replace('*\\.', '*.')
print(result, file=open(sys.argv[3], 'w'))
