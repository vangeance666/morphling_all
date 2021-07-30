layout.submit = (function() {

	var self = {};

	var titleCtx = ["h2", {"class": "text-center display-4"}, "Malware Sample Upload"];
	
	var genOptionsCtx = function(labelText, checkedValue) {
		return ["div", { "class": "form-check form-check-inline" },
			["input", {
				"class": "form-check-input",
				"type": "checkbox",
				"id": "inlineCheckbox1",
				"value": checkedValue,
				"/": "/"
			}
			],
			["label", { "class": "form-check-label", "for": "inlineCheckbox1" },
				labelText
			]
		];
	};

	var uploadInputCtx = 
	["div", {"class": "input-group"},
	    ["div", {"class": "custom-file"},
	        ["input", {
	                "class": "custom-file-input my-file-input",
	                "type": "file",
	                "id": ids['submitUploadInput']
	            }
	        ],
	        ["label", {"id": ids['submitUploadInputLabel'], "class": "custom-file-label", "for": ids['homeApkInput']},
	            "Choose sample to submit"
	        ]
	    ]
	];

	var optionsCtx = ['div', {'class': 'text-center pt-2'},
		tuningOptions['data'], function(x){
		return genOptionsCtx(x['name'], x['value'])
	}];

	var optionsRowCtx = ['div', {'class': 'row justify-content-center'},
		optionsCtx
	];

	var submitRowCtx = ['div', {'class': 'row justify-content-center'},
		["button", {"id": ids['submitUploadBtn'], "class": "mt-5 btn btn-md btn-block btn-primary"}, "Submit"],
	];

	var machineNamesSelectCtx = ["select", {'id': ids['submitMachineSelect'], "class": "form-select", "aria-label": "Default select example"},
	    ["option", {"selected": "selected"}, "Open this select menu"]
	    // ["option", {"value": "1"}, "One"],
	    // ["option", {"value": "2"}, "Two"],
	    // ["option", {"value": "3"}, "Three"]
	]


	self.bodyCtx = ['div', {'class': 'pt-1 container'},
		titleCtx,
		uploadInputCtx,
		// optionsRowCtx,
		machineNamesSelectCtx,
		submitRowCtx
	];
	
	var addEvents = function() {
		// 1 Clicking of file input
		// 2 click of submit button
		$('#'+ids['submitUploadInput']).click(function(e){
			e.preventDefault();
			console.log("selecting sample file");
			window.needsUpdate.submitPromptFile = true;
		});

		$('#'+ids['submitUploadBtn']).click(function(e){
			e.preventDefault();
			console.log('clicked submit sample button');
			data.chosenMachine = $('#submit-machine-select').val()
			window.needsUpdate.submitSendFile = true;
		})
		console.log("Finished adding submit js events");
	};

	self.setFileLabel = function(name) {
		$('#'+ids['submitUploadInputLabel']).text(name);
	}

	self.getFileLabel = function() {
		return $('#'+ids['submitUploadInputLabel']).text();
	}

	var updateMachineNames = function() {
		console.log("set gaetmachines names to true")
		window.needsUpdate.getMachineNames = true;
	}

 	self.setMachinesSelect = function() {
 		console.log("setMachinesselect");
 		console.log("data.machineNames: "+ data.machineNames)
 		if (data.machineNames) {
 			console.log("Have data machine names");

 			$('#'+ids['submitMachineSelect']).html(
 				HTML(["option", {"selected": "selected"},
 					 	"Open this select menu"
 					], data.machineNames, function(n) {
				 		return ["option", {"value": n}, n]
				 	})
 			);
 		}
 	}

	self.display = function() {
		$('#'+ids['bodyRoot']).html(HTML(self.bodyCtx));
		$('nav .nav-item').removeClass('active');
		$('#'+ids['navSubmitItem']).addClass('active');

		addEvents();
		updateMachineNames();
	}

	return self;
})()