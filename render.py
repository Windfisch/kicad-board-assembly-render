import sys
import os

infile = sys.argv[1]
outdir = sys.argv[2]
outpattern = sys.argv[3]
resolution_x = int(sys.argv[4])
resolution_y = int(sys.argv[5])

if "%" in outpattern:
	[outprefix, outsuffix] = outpattern.split("%")
else:
	outprefix = outpattern
	outsuffix = ""

outfile = "temp.kicad_pcb"

args = sys.argv[6:]

try:
	tool_args = args[args.index("--") + 1 : ]
	args = args[: args.index("--")]
except ValueError:
	tool_args = []
	pass


footprints = []
for i, additional_footprints in enumerate(args):
	print("########## Step %d ##########")

	footprints.append(additional_footprints)
	print("python %s/set_footprint_visibility.py %s %s %s" % (os.path.dirname(__file__), ",".join(footprints), infile, outfile))
	os.system("python %s/set_footprint_visibility.py %s %s %s" % (os.path.dirname(__file__), ",".join(footprints), infile, outfile))

	print("pcbnew_do --rec_width %d --rec_height %d 3d_view %s %s %s" % (resolution_x, resolution_y, " ".join(tool_args), outfile, outdir))
	os.system("pcbnew_do --rec_width %d --rec_height %d 3d_view %s %s %s" % (resolution_x, resolution_y, " ".join(tool_args), outfile, outdir))

	os.system("mv %s/capture.png %s/orig_%s%02d%s.png" % (outdir, outdir, outprefix, i, outsuffix))

	if i == 0:
		os.system("cp %s/orig_%s%02d%s.png %s/%s%02d%s.png" % (outdir, outprefix, i, outsuffix, outdir, outprefix, i, outsuffix))
	else:
		os.system("python imgdiff.py %s/orig_%s%02d%s.png %s/orig_%s%02d%s.png %s/%s%02d%s.png" % (outdir, outprefix, i, outsuffix, outdir, outprefix, i-1, outsuffix, outdir, outprefix, i, outsuffix))
