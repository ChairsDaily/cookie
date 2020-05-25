#!/usr/bin/python3
"""
Beautiful command line parsing 
@author chairs
"""
import inspect, sys
from collections import namedtuple
from collections import defaultdict
from subprocess import DEVNULL

class Cookie (object):
	"""
	Main decorator object
	@param name of application 
	"""

	def __init__ (self, app_name, notes=()):

		self.optarg = namedtuple('optarg', 
			['full', 'abbrev', 'default'])
		self.name = str(app_name)
		self.notes = notes

	def __parse (self, args):
		"""
		Parse command line arguments from argv, built to be simple
		and as fast as possible to avoid application overhead
		@param command line arguments 
		@return necessary destinations and identifiers
		"""
		ordered = list(); full = abbrev = dict()
		args = args + ['']

		i = 0
		while i < len(args) - 1:
			token = args[i]
			next_token = args[i + 1]

			# the full argument case
			if token.startswith('--'):
				if next_token.startswith('-'): 
					raise ValueError('{} incomplete'.format(token))
				else:
					full[token[2:]] = next_token
					i += 2

			# the shorthand argument case (more common)
			elif token.startswith('-'): 
				if next_token.startswith('-'):
					raise ValueError('{} incomplete'.format(token))
				else:
					abbrev[token[1:]] = next_token
					i += 2

			else: 
				ordered.append(token)
				i += 1

		return ordered, full, abbrev


	def __construct_ordered (self, params):
		"""
		Build the ordered parameters (those without flags, positional)
		@param parameters from parse 
		@return all exclusively oredered arguments
		"""
		return [key for key, arg in params.items() if arg.default == inspect._empty]

	def __construct_optional (self, params):
		"""
		Build the optional parameters (those with flags, switches)
		@param parameters from parse
		@return all exclusively optional arguments
		"""
		args = []
		filtered = {
			key: arg.default for key, arg in params.items() if arg.default != inspect._empty}
		
		for key, default in filtered.items():
			arg = self.optarg(full=key, abbrev=key[0].lower(), default=default)
			args.append(arg)

		args_full = args_abbrev = dict()

		# resolve possible conflicts
		known_count = defaultdict(int)
		for arg in args:
			args_full[arg.full] = arg

			if known_count[arg.abbrev] == 0: args_abbrev[arg.abbrev] = arg
			elif known_count[arg.abbrev] == 1: 

				# establish abbreviation
				new_abbrev = arg.apprev.upper()
				args_full[arg.full] = self.optarg(
					full=arg.full, 
					abbrev=new_abbrev, 
					default=arg.default)
				args_abbrev[new_abbrev] = args_full[arg.full]
			else:
				new_abbrev = arg.apprev.upper() + str(known_count[arg.abbrev])
				args_full[arg.full] = self.optarg(
					full=arg.full,
					abbrev=new_abbrev,
					default=arg.default)
				args_abbrev[new_abbrev] = args_full[arg.full]

			known_count[arg.abbrev] += 1

		return args_full, args_abbrev


	def __resolve (self, args, signature):
		"""
		Resolve arguments final destinations
		@param args arguments from construction
		@param signatures
		@return final destinations
		"""
		ordered, opt_parsed_full, opt_parsed_abbrev = self.__parse(args[1:])

		ordered_def = self.__construct_ordered(signature.parameters)
		if len(ordered) != len(ordered_def):
			raise Exception('wrong number of oredered arguments')

		opt_parsed = dict()
		opt_parsed.update(opt_parsed_full)
		opt_parsed.update(opt_parsed_abbrev)

		opt_def_full, opt_def_abbrev = self.__construct_optional(signature.parameters)
		optional = {o.full: o.default for o in opt_def_full.values()}
		opt_def = dict()
		opt_def.update(opt_def_full)
		opt_def.update(opt_def_abbrev)

		for key, value in opt_parsed.items():
			if key not in opt_def: raise Exception('resolution error')
			d = opt_def[key]
			optional[d.full] = value

		return ordered, optional


	def __usage_outline (self, signature):
		"""
		Nice formatted help message to outline usage
		@param signature for arguments
		"""
		ordered = self.__construct_ordered(signature.parameters)
		full, _ = self.__construct_optional(signature.parameters)

		ordered_str = ' '.join(name.upper() for name in ordered)
		optional_str = ' '.join('\n[-{} | --{} {}],'.format(

			opt.abbrev, opt.full, opt.full.upper()) for opt in full.values()) 
		optional_str = ''.join(optional_str.split(',')[::2])


		return '{} {}'.format(ordered_str, optional_str)


	def get_args (self, function):
		"""
		The main decorator, the glue
		"""
		def wrapper ():
			sig = inspect.signature(function)
			try:
				ordered, optional = self.__resolve(sys.argv, sig)
			except Exception:

				self.outline = ('Usage: ', sys.argv[0], self.__usage_outline(sig,)) 
				print(*self.outline)
				if not self.notes == (): 
					print('\n'.join(self.notes) + '\n'+'\t'*1 + 'respectively')
				return 

			function(*ordered, **optional)

		return wrapper 

	def run (self, function_name, silent=False):
		restore = sys.stdout
		if silent:
			sys.stdout = open('/dev/null', 'w').close()
		function_name()
		sys.stdout = restore

