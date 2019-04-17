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
lg.add('_', r'_')
lg.add('...', r'\.\.\.')

name_excludes = r'[^(),:[\] ]'
lg.add('NAME', name_excludes + r'+')

lg.ignore(r'\s+')

class Expr:
	def __init__(self, v):
		self.v = v

	def eval(self, ctx=None):
		return self.v.eval(ctx)

	def match_pn(self, x):
		return self.v.match_pn(x)

class Name:
	def __init__(self, v):
		self.v = v

	def eval(self, ctx):
		if self.v in ctx:
			return ctx[self.v]

		print(f'{self.v} is undefined')
		return # TODO error

class Number:
	def __init__(self, v):
		self.v = v

	def eval(self, ctx):
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

	def eval(self, ctx):
		return tuple(v.eval(ctx) for v in self.v)

	def match_pn(self, x):
		if len(self.v) == 1:
			if type(x) is not tuple or len(x) > 1:
				return self.v[0].match_pn(x)
		elif type(x) is not tuple:
			return None

		j = 0
		ctx = {}
		for i, v in enumerate(self.v):
			if type(v.eval()) is PnVarargEmpty:
				rem = len(self.v) - (i + 1)
				if i + rem > len(x): # (:x, ..., :y) should not match (1) to be { x = 1, y = 1 }
					return None

				j = len(x) - rem
				continue

			if j >= len(x):
				return None

			subctx = v.match_pn(x[j])
			if subctx is None:
				return None

			ctx = { **ctx, **subctx }
			j += 1

		return ctx

class PnVar:
	def __init__(self, name):
		self.name = name

	def eval(self, ctx):
		return self

	def match_pn(self, x):
		return { self.name: x }

class PnEmpty:
	def eval(self, ctx):
		return self

	def match_pn(self, x):
		return {}

class PnVarargEmpty:
	def eval(self, ctx):
		return self

	def match_pn(self, x):
		return {}

class Function:
	def __init__(self, name, branches):
		self.name = name
		self.branches = branches

	def __call__(self, arg):
		for brch in self.branches:
			ctx = brch[0].match_pn(arg)
			if ctx is not None:
				return brch[1].eval(ctx)

		print(f'no matching branch in "{self.name}" for input "{arg}"')
		return # TODO error

	def eval(self, _):
		return self

	def match_pn(self, x):
		return {} if self is x else None

class FuncCall:
	def __init__(self, fn, arg):
		self.fn = fn
		self.arg = arg

	def eval(self, ctx):
		if self.fn not in func_table:
			print(f'function "{self.fn}" is not defined')
			return # TODO error

		arg = self.arg.eval(ctx)
		return func_table[self.fn](arg)

func_table = {}
pg = ParserGenerator(['FLOAT', 'INT', '(', ')', '_', '...', ',', ':', '[', ']', 'fx', 'NAME'])

@pg.production('expr : func')
@pg.production('expr : tuple')
@pg.production('expr : pnvar')
@pg.production('expr : pn-empty')
@pg.production('expr : pn-vararg-empty')
@pg.production('expr : number')
@pg.production('expr : func-call')
@pg.production('expr : name')
def expr(p):
	return Expr(p[0])

@pg.production('name : NAME')
def expr_name(p):
	return Expr(Name(p[0].getstr()))

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

@pg.production('pn-empty : _')
def pn_empty(p):
	return PnEmpty()

@pg.production('pn-vararg-empty : ...')
def pn_vararg_empty(p):
	return PnVarargEmpty()

@pg.production('func : fx NAME func-body')
def func(p):
	f = Function(p[1].getstr(), p[2])
	func_table[f.name] = f
	return f

@pg.production('func-body : [ tuple expr func-body')
def func_body_more(p):
	p[3].insert(0, (p[1], p[2]))
	return p[3]

@pg.production('func-body : [ tuple expr')
def func_body(p):
	return [(p[1], p[2])]

@pg.production('func-call : expr ] NAME')
def func_call(p):
	return FuncCall(p[2].getstr(), p[0])

lexer = lg.build()
parser = pg.build()

def parse(expr):
	return parser.parse(lexer.lex(expr))
