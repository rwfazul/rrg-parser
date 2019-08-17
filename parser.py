import utils as u
import string, random, copy

class Parser:
	def __init__(self, grammar, orientation):
		self.grammar = grammar
		self.non_terminals = grammar[u.NON_TERMINALS_KEY]
		self.terminals = grammar[u.TERMINALS_KEY]
		self.productions = grammar[u.PRODUCTIONS_KEY]
		self.start_symbol = grammar[u.START_SYMBOL_KEY]
		self.start_prod = self.productions[self.start_symbol]
		self.errors = []
		self.orientation = orientation
		self.validate_orientation()
		self.validate_grammar()
		self.applied_productions = []

	def validate(self, sentence):
		self.lex_validate(sentence.strip())
		assert self.find_path(sentence.strip(), self.start_prod), self.get_sintax_error(sentence.strip(), max(self.errors))
 
	def find_path(self, sentence, production_right, cursor=0):
		if self.end_of_sentence(sentence, cursor):
			if self.has_empty_derivation(production_right):
				return True
			else:
				self.add_sintax_error(cursor)
				return False
		for p in production_right:
			if self.match(sentence[cursor], p[self.TERMINAL]):
				match_next_terminals = True
				cursor_last_terminal = cursor
				for next_terminal in range(self.TERMINAL + 1, self.get_pos_last_terminal(p)):	
					cursor_last_terminal = cursor_last_terminal + 1
					if not self.match(sentence[cursor_last_terminal], p[next_terminal]):
						match_next_terminals = False
						break
				if match_next_terminals:
					self.applied_productions.insert(cursor, p)
					if self.find_path(sentence, self.navigate(p), self.next(cursor_last_terminal)):
						return True
		self.add_sintax_error(cursor)
		return False

	def navigate(self, prod):
		return self.productions[prod[self.NON_TERMINAL]]

	@staticmethod
	def end_of_sentence(sentence, cursor):
		return len(sentence) == cursor

	def has_empty_derivation(self, production):
		return self.EMPTY in production

	@staticmethod
	def match(a, b):
		return a == b

	@staticmethod
	def next(cursor):
		return cursor + 1
	
	def get_pos_last_terminal(self, p):
		return self.NON_TERMINAL + len(p)

	def add_sintax_error(self, cursor):
		self.errors.append(cursor)

	def get_sintax_error(self, sentence, pos):
		str_err = u.str_error_pointer(pos + 1)
		if pos >= len(sentence):
			return str_err + u.str_not_final_state(sentence[-1], pos) 
		return str_err + u.str_unexpected_char(sentence[pos], pos + 1)

	def lex_validate(self, sentence):
		for i, c in enumerate(sentence):
			assert self.is_terminal(c), self.get_lex_error(sentence, i)
		self.errors = []
		self.applied_productions = []

	def get_lex_error(self, sentence, pos):
		return  u.str_error_pointer(pos + 1) + u.str_unexpected_char(sentence[pos], pos + 1, lex=True)

	def validate_orientation(self):
		assert self.orientation in u.GRAMMAR_ORIENTATIONS, u.str_not_valid_orientation(self.orientation)
		self.TERMINAL = u.get_terminal_pos(self.orientation)
		self.NON_TERMINAL = u.get_non_terminal_pos(self.orientation)
		self.EMPTY = u.EMPTY

	def validate_grammar(self):
		assert self.start_symbol in self.non_terminals, u.str_invalid_strat_symbol(self.start_symbol, self.non_terminals)
		assert not set(self.terminals).intersection(self.non_terminals), u.str_term_in_non_term(self.terminals, self.non_terminals)
		assert len(self.productions.keys()) is len(set(self.productions.keys())), u.str_multiple_productions()
		raw_productions = copy.deepcopy(self.productions)
		for left, right in raw_productions.items():
			assert left in self.non_terminals, u.str_invalid_left_side(left, self.non_terminals)
			for handle in right:
				self.is_valid_right_production_side(left, handle)
			
	def is_valid_right_production_side(self, left, handle):
		if len(handle) > 1:
			assert self.is_terminal(handle[self.TERMINAL]), u.str_invalid_right_side(self.orientation, left, handle, handle[self.TERMINAL], terminal=True)
			assert self.is_non_terminal(handle[self.NON_TERMINAL]), u.str_invalid_right_side(self.orientation, left, handle, handle[self.NON_TERMINAL], non_terminal=True)
		else:
			assert self.is_empty(handle[self.TERMINAL]) or self.is_terminal(handle[self.TERMINAL]), u.str_invalid_right_side(self.orientation, left, handle, handle[self.TERMINAL], terminal=True)
			if self.is_terminal(handle[self.TERMINAL]):
				new_state = self.create_new_state()
				self.non_terminals.append(new_state)
				self.productions[left].remove(handle)
				self.productions[left].append("{}{}".format(handle, new_state))
				self.productions[new_state] = [self.EMPTY]

	def is_terminal(self, c):
		return c in self.terminals

	def is_non_terminal(self, c):
		return c in self.non_terminals
	
	def is_empty(self, c):
		return c is self.EMPTY

	def create_new_state(self):
		new_state = random.choice(string.ascii_uppercase)
		while new_state in self.productions:
			new_state = random.choice(string.ascii_uppercase)
		return new_state
