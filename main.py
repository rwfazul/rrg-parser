import sys, json
from jsonschema import validate
from schema import grammar_schema
from parser import Parser

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

	print("* Grammar is valid!")
	print("* Type the sentences (exit() to quit)...")

	while (True):
		try:	
			raw_sentence = input("> ")
			sentence = raw_sentence.strip()
			if sentence == 'exit()':
				handle_exception("bye!", exit=True)
			if sentence:
				parser.validate(sentence)
				print("the sentence is valid!")
				print("moviments: {}".format(parser.start_symbol), end="->")
				for p in parser.applied_productions:
					print(p, end="->")
				print("$")
		except AssertionError as e:
			if len(raw_sentence.lstrip()) < len(raw_sentence):
				print("< {}".format(sentence))
			handle_exception(e, exit=False)
		except Exception as e:
			handle_exception("[unexpected error] {} {}".format(e, "want to quit? use exit()"), exit=False)

if __name__ == "__main__":
    main()
