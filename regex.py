import sys, json
from jsonschema import validate
from schema import grammar_schema
from parser import Parser
from greenery import fsm, lego

def get_grammar():
	try:
		raw_grammar = None
		with open(sys.argv[1], 'r') as file:
			raw_grammar = file.read()
		grammar = json.loads(raw_grammar)
		validate(instance=grammar, schema=grammar_schema)
		return grammar
	except IndexError as e:
		handle_exception("[usage example] $ python3 {} grammar.txt".format(sys.argv[0]))
	except FileNotFoundError as e:
		handle_exception("[error] grammar file '{}' not found".format(sys.argv[1]))
	except json.decoder.JSONDecodeError as e:
		handle_exception("[error] gramar file '{}' is not well formated:\n\t- {}".format(sys.argv[1], e))
	except Exception as e:
		handle_exception("[unexpected error] {}".format(e))

def get_parser(grammar):
	try:
		parser = Parser(grammar, orientation='right')
		return parser
	except AssertionError as e:
		handle_exception(e)
	except Exception as e:
		handle_exception("[unexpected error] {}".format(e))

def handle_exception(msg, exit=True):
	print(msg)
	if exit:
		sys.exit()

def main():
	grammar = get_grammar()
	parser = get_parser(grammar)

	finals=[]
	productions={}
	for left, right in parser.productions.items():
		for handle in right:
			if handle is not parser.EMPTY:
				if left not in productions:
					productions[left] = {}
				productions[left][handle[0]] = handle[1]
			else:
				finals.append(left)
	machine = fsm.fsm(
		alphabet = set(parser.terminals),
		states = set(parser.non_terminals),
		initial = parser.start_symbol,
		finals = set(finals),
		map = productions
	)
	rex = lego.from_fsm(machine)
	print(machine)
	print(rex)

if __name__ == "__main__":
    main()
