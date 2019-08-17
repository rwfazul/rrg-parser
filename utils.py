# grammar
NON_TERMINALS_KEY='N'
TERMINALS_KEY='T'
PRODUCTIONS_KEY='P'
START_SYMBOL_KEY='S'

EMPTY=' '
GRAMMAR_ORIENTATIONS=['left', 'right']
def get_terminal_pos(orientation):
	# LEFT_TERMINAL_POS=1
	# RIGHT_TERMINAL_POS=0
	return orientation is 'left' 

def get_non_terminal_pos(orientation):
	# LEFT_NON_TERMINAL_POS=0
	# RIGHT_NON_TERMINAL_POS=-1
	return -(orientation is 'right')

# errors
def str_error_pointer(offset):
	return '{:>{}}\n'.format('^', offset + len("> "))
	
def str_not_final_state(char, pos):
	return "[sintax error] charactere '{}' at pos {} is not in a final state".format(char, pos) 

def str_unexpected_char(char, pos, lex=False):
	return "[{} error] unexpected character '{}' at pos {}".format("lex" if lex else "sintax", char, pos)

def str_not_valid_orientation(orientation):	
	return "[invalid grammar orientation] '{}' is not a valid grammar orientation (should be 'left' or 'right')".format(orientation)

def str_invalid_start_symbol(start, non_terminals):
	return "[invalid start symbol] start symbol '{}' is not in non-terminals ({})".format(start, non_terminals)

def str_term_in_non_term(terminals, non_terminals):
	return "[invalid symbols] there is a intersection between terminals and non-terminals ({})".format(set(terminals).intersection(non_terminals)) 

def str_multiple_productions():
	return "[production error] non-terminals in left side of production should be unique"

def str_invalid_left_side(left, non_terminals):
	return "[invalid production] production '{}' is not in non-terminals ('{}')".format(left, non_terminals)
	
def str_invalid_right_side(orientation, left, right, char, terminal=False, non_terminal=False):
	char_type=None	
	if terminal:				
		char_type="terminals"
	elif non_terminal:
		char_type="non-terminals"	
	if char_type:
		return "[invalid production] production with invalid right side '{} -> {}' ({}-regular grammar, charactere '{}' is not in {})".format(left, right, orientation, char, char_type)
