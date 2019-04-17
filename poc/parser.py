from rply import ParserGenerator, LexerGenerator

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

name_excludes = r'[^(),:[\] ]'
lg.add('NAME', name_excludes + r'+')

lg.ignore(r'\s+')

class Number:
	def __init__(self, v):
		self.v = v

	def eval(self, ctx=None):
		return self.v

	def match_pn(self, x):
		return {} if self.v == x else None

class Tuple:
	def __init__(self, v=None):
		self.v = [] if v is None else [v]

	def prepend(self, v):
		self.v.insert(0, v)

	def append(self, v):
		self.v.append(0, v)

	def eval(self, ctx=None):
		return [v.eval(ctx) for v in self.v]

	def match_pn(self, x):
		# arg is not tuple
		if type(x) is not Tuple:
			return None if len(self.v) > 1 else self.v[0].match_pn(x)

		ctx = {}
		for v, a in zip(self.v, x.v):
			subctx = v.match_pn(a, ctx)
			if subctx is None: # match failed
				return None

			ctx = { **ctx, **subctx }

		return ctx

class PnVar:
	def __init__(self, name):
		self.name = name

	def eval(self, ctx=None):
		return self

class Function:
	def __init__(self, name, body):
		self.name = name
		self.branches = body.branches

	def __call__(self, arg):
		for brch in self.branches:
			ctx = brch[0].match_pn(arg)
			if ctx is not None:
				return brch[1].eval(ctx)

		print(f'no matching branch in "{self.name}" for input "{arg}"')
		return # TODO error

	def eval(self):
		return self

class FuncBody:
	def __init__(self, arg, expr):
		self.branches = [(arg, expr)]

	def argmatch(self, arg):
		return True

	def add(self, arg, expr):
		self.branches.insert(0, (arg, expr))

class FuncCall:
	def __init__(self, fn, arg):
		self.fn = fn
		self.arg = arg

	def eval(self, ctx=None):
		if self.fn not in func_table:
			print(f'function "{self.fn}" is not defined')
			return # TODO error

		arg = self.arg.eval(ctx)
		return func_table[self.fn](arg)

func_table = {}
pg = ParserGenerator(['FLOAT', 'INT', '(', ')', ',', ':', '[', ']', 'fx', 'NAME'])

@pg.production('expr : func')
@pg.production('expr : tuple')
@pg.production('expr : pnvar')
@pg.production('expr : number')
@pg.production('expr : func-call')
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
	f = Function(p[1].getstr(), p[2])
	func_table[f.name] = f
	return f

@pg.production('func-body : [ tuple expr func-body')
def func_body_more(p):
	p[3].add(p[1], p[2])
	return p[3]

@pg.production('func-body : [ tuple expr')
def func_body(p):
	return FuncBody(p[1], p[2])

@pg.production('func-call : expr ] NAME')
def func_call(p):
	return FuncCall(p[2].getstr(), p[0])

lexer = lg.build()
parser = pg.build()

def parse(expr):
	return parser.parse(lexer.lex(expr))
