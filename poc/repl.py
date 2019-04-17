import sys
from parser import parse

def repl(ln):
	ln = ln.strip()
	if not ln:
		return

	v = parse(ln).eval()
	if v is not None:
		print(v)

def repl_from_file(fn):
	with open(fn) as f:
		for ln in f:
			ln = ln.strip()
			if ln:
				print('fx >', ln)
				repl(ln)

def main(fn=None):
	while True:
		ln = input('fx > ')
		repl(ln)

if __name__ == '__main__':
	if len(sys.argv) > 1:
		repl_from_file(sys.argv[1])
	else:
		main()
