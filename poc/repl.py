from parser import parse

def main():
	while True:
		expr = input('fx > ')
		val = parse(expr).eval()
		print(val)

if __name__ == '__main__':
	main()
