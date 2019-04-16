from rply import ParserGenerator, LexerGenerator

class Number:
	def __init__(self, v):
		self.v = v

	def eval(self):
		return self.v

class Tuple:
	def __init__(self, v):
		self.v = [v]

	def prepend(self, v):
		self.v.insert(0, v)

	def eval(self):
		return [v.eval() for v in self.v]

class PnVar:
	def __init__(self, name):
		self.name = name

	def eval(self):
		return self

class Function:
	def __init__(self, name, body):
		self.name = name
		self.body = body

	def eval(self):
		return self

class FuncBody:
	def __init__(self, arg, expr):
		self.forks = [(arg, expr)]

	def add(self, arg, expr):
		self.bodies.insert(0, (arg, expr))

	def eval(self):
		return self

lg = LexerGenerator()

lg.add('FLOAT', r'(-|\+)?[0-9]+\.[0-9]*')
lg.add('INT', r'(-|\+)?[0-9]+')
lg.add('(', r'\(')
lg.add(')', r'\)')
lg.add(',', r',')
lg.add(':', r':')
lg.add('[', r'\[')
lg.add(']', r'\]')
lg.add('fx', r'fx')

name_excludes = r'[^(),:[\]]'
lg.add('NAME', name_excludes + r'+')

lg.ignore(r'\s+')

pg = ParserGenerator(['FLOAT', 'INT', '(', ')', ',', ':', '[', 'fx', 'NAME'])

@pg.production('expr : func')
@pg.production('expr : tuple')
@pg.production('expr : pnvar')
@pg.production('expr : number')
def expr(p):
	return p[0]

@pg.production('tuple : ( expr )')
def tuple_expr(p):
	return Tuple(p[1])

@pg.production('tuple : ( expr tuple-rest )')
def tuple_exprs(p):
	p[2].prepend(p[1])
	return p[2]

@pg.production('tuple-rest : , expr')
def tuple_rest(p):
	return Tuple(p[1])

@pg.production('tuple-rest : , expr tuple-rest')
def tuple_rest_more(p):
	p[2].prepend(p[1])
	return p[2]

@pg.production('number : INT')
@pg.production('number : FLOAT')
def number(p):
	numtype = p[0].gettokentype()
	if numtype == 'INT':
		return Number(int(p[0].getstr()))
	elif numtype == 'FLOAT':
		return Number(float(p[0].getstr()))

@pg.production('pnvar : : NAME')
def pnvar(p):
	return PnVar(p[1].getstr())

@pg.production('func : fx NAME func-body')
def func(p):
	return Function(p[1].getstr(), p[2])

@pg.production('func-body : [ tuple expr func-body')
def func_body_more(p):
	p[3].add(p[1], p[2])
	return p[3]

@pg.production('func-body : [ tuple expr')
def func_body(p):
	print(p)
	return FuncBody(p[1], p[2])

lexer = lg.build()
parser = pg.build()

def parse(expr):
	return parser.parse(lexer.lex(expr))
