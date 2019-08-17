grammar_schema = {
	"title": "grammar",
	"type": "object",
	"properties": {
	    "N": {
		"type": "array",
		"items": {
			"type": "string",
			"minLength": 1,
			"maxLength": 1
		}
	    },
	    "T": {
		"type": "array",
		"items": {
			"type": "string",
			"minLength": 1,
			"maxLength": 1
		}
	    },
	    "P": {
		"title": "production",
		"type": "object",
		"patternProperties": {
			"^.$": { 
				"type": "array",
				"items": {
					"type": "string",
					"pattern": "^(.)+$"
				}
			}
		}  
	    },
	    "S": {
		"type": "string",
		"minLength": 1,
		"maxLength": 1
	    }
	},
	"required": [ "N", "T", "P", "S" ]
}
