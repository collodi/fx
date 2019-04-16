from rply import ParserGenerator, LexerGenerator

class Number:
	def __init__(self, v):
		self.v = v

	def eval(self):
		return self.v

class Tuple:
	def __init__(self, v1, v2=None):
		self.v = [v1]
		if v2 is not None:
			self.v += v2.v

	def eval(self):
		return [v.eval() for v in self.v]

lg = LexerGenerator()

lg.add('FLOAT', r'(-|\+)?[0-9]+\.[0-9]*')
lg.add('INT', r'(-|\+)?[0-9]+')
lg.add('(', r'\(')
lg.add(')', r'\)')
lg.add(',', r',')

lg.ignore(r'\s+')

pg = ParserGenerator(['FLOAT', 'INT', '(', ')', ','])

@pg.production('expr : number')
def expr_number(p):
	return Number(p[0])

@pg.production('expr : tuple')
def expr_tuple(p):
	return p[0]

@pg.production('tuple : ( expr )')
def tuple_expr(p):
	return Tuple(p[1])

@pg.production('tuple : ( expr more-expr )')
def tuple_exprs(p):
	return Tuple(p[1], p[2])

@pg.production('more-expr : , expr')
@pg.production('more-expr : , expr more-expr')
def more_expr(p):
	if len(p) == 2:
		return Tuple(p[1])

	return Tuple(p[1], p[2])

@pg.production('number : INT')
@pg.production('number : FLOAT')
def number(p):
	numtype = p[0].gettokentype()
	if numtype == 'INT':
		return int(p[0].getstr())
	elif numtype == 'FLOAT':
		return float(p[0].getstr())

lexer = lg.build()
parser = pg.build()

def parse(expr):
	return parser.parse(lexer.lex(expr))
