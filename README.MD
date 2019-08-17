# rrg-parser

-------------------------------

- Requirements:
	+ Python v3+
	+ jsonschema ($ pip install jsonschema)

-------------------------------

- Grammar definition (textfile, e.g. 'grammar.txt'):
	+ Right regular grammar G = (N, T, P, S) in JSON format with the following definitions:
		- list of non-terminal symbols ("N"), e.g. "N": ["A", "B"]
		- list of terminal symbols ("T"), e.g. "T": ["a", "b, "c"]
		- nested JSON object for the production rules ("P"), where which productions is defined as:
		
		```
			- <non-terminal>: [<terminal><non-terminal>, ...], e.g. "A": ["aA", "bB"]
			- <terminal>: [<terminal>...<terminal><non-terminal>, ...], e.g. "A": ["abaA", "bB"]
			- <non-terminal>: [<terminal>, ... ], e.g. "A": ["aA", "a"]
			- <non-terminal>: [<terminal>...<terminal>, ... ], e.g. "A": ["aA", "bbb"]
			- <non-terminal>: [empty (" "), ...], e.g. "A": [bB, " "]
		```
		- start symbol in the grammar (S), e.g. "S" : "B"
		
	+ Example: 'grammar.txt'
	
	```json
		{
			"N": ["S","A"],
			"T": ["a", "b", "c"],
			"P": {
				"S": ["aS", "bA"],
				"A": ["cA", " "]
			},
			"S": "S"
		}
	```
-------------------------------

- Running:

```bash
	$ python3 main.py grammar.txt
```
-------------------------------

- If the grammar is valid, it will be prompted in execution time a sequence of words (type Ctrl+C or exit() to exit)
	+ If a word belongs to L(G), a message and the list of productions (derivation) applied during the syntax analysis will be printed;
	+ Otherwise, the parser will show the cause and position of the error (lexical or syntax) 

-------------------------------

- Demo (generator of regular expressions):
```bash
	$ pip install greenery
	$ python3 regex.py grammar.txt
```
-------------------------------
