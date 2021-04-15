import os
import subprocess

args = os.sys.argv
if 1 == len(args):
	exit

for in_path in args[1:]:
	out_path = in_path.replace('.avi', '.mp4').replace('.mp4', '_265.mp4')
	cmd = 'ffmpeg -i "{}" -c:a copy -c:v libx265 -crf 28 "{}"'.format(in_path, out_path)
	subprocess.call(cmd)
