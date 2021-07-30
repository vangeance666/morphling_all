layout.task = (function() {

	var self = {};

	// var 

	var genResultsDataRowsCtx = function(resultsData) {
		console.log("resultsData", resultsData);

		var ret = [];
		for (const row of resultsData){
			for (const key in row) {
				console.log("key:", key);
				console.log("data[key]:", data[key]);
				ret.push(['p', ['b', key], " : "+row[key]]);
			}
		}
		return ret;
	}


	var genTaskExpandDetailsCtx = function(taskData) {
		
		if (taskData['status'] != "evaluated") {
			return ['p', 'Task not evaluated yet']
		}

		var sigs = [['h4', {'class': 'pl-1'}, 'Local Signatures Flagged']];
		var tuners = [['h4', {'class': 'pl-1'}, 'Tuners applied']];


		if ("signatures" in taskData) {
			for (const signatures of taskData['signatures']) {
				console.log("signatures", signatures);
				
				var sigNameHeader = ['button', {
						'class': 'btn btn-danger',
						'data-toggle': 'collapse',
						'data-target': '#collapse-signature-'+signatures['name']
					}, signatures['name']
				];

				console.log("sigNameHeader", sigNameHeader);


				var sigResults = ['div', {
					'id': 'collapse-signature-'+signatures['name'],
					'class': 'collapse'},
					genResultsDataRowsCtx(signatures['data'])
				];

				sigs.push([sigNameHeader, sigResults])
			}
		}

		if ("tuners_to_apply" in taskData) {
			for (const tuner of taskData['tuners_to_apply']) {

				var tunerNameHeader = ['button', {
						'class': 'btn btn-success',
						'data-toggle': 'collapse',
						'data-target': 'collapse-tuner-'+tuner['name']
						// "aria-expanded": "false",
      //   				"aria-controls": 'collapse-tuner-'+tuner['name']
					}, tuner['name']
				]

				var tunerResults = ['div', {
						'id': 'collapse-tuner-'+tuner['name'],
						'class': 'collapse'
					}, genResultsDataRowsCtx(tuner['data'])
				];
				console.log("tunerResults", tunerResults);

				tuners.push([tunerNameHeader, tunerResults])

			}
		}

		if (sigs.length == 1) {
			sigs.push(['p', "No sigs found"])
		}
		if (tuners.length == 1) {
			tuners.push(['p', "No tuners found"])
		}

		console.log("[sigs, tuners]", [sigs, tuners]);
		return [sigs, tuners];
			
	}

	var _formatPrevTask = function(prevTask) {
		if (prevTask != null) {
			return ["a", {'class': ''+eleClass['taskPrevTaskBtn'], "href": "#task"}, prevTask['id']];
		}
		return "None"
	}

	var genTableRowCtx = function(taskData) {
		return [
		    ["tr", {"data-widget": "expandable-table", "aria-expanded": "false"},
		        ['td', taskData['id'] ],
		        ['td', taskData['file_path'] ],
		        ['td', taskData['machine_name'] ],
		        ['td', taskData['mal_score'] ],
		        ['td', taskData['status'] ],
		        ['td', taskData['resubmited'] ],
		        ['td', _formatPrevTask(taskData['previous_task'])],
		        ['td', { 'id': ids['taskActionCol'], 'class': 'text-center'},
		        	['i', {'class': 'fas fa-hand-paper '+eleClass['taskActionBtn'],
			        		'data-toggle': 'tooltip',
			        		'data-placement': 'top',
			        		'title': 'Exclude task from being evaluated & resumbmited'
		        		}
		        	]
		        ]		       	
		    ],
		    ["tr", {"class": "expandable-body d-none"},
		        ["td", {"colspan": "6"}, 
		        	// "hehe"
		        		genTaskExpandDetailsCtx(taskData),
		        ] 
		    ]
		];
	}

	// later put color
	var genScoresCtx = function(scores) {
		ret = [];
		for (var i = 0; i < taskIds.length; ++i) {
			ret.push(["a", taskIds[i]]);
		}
		return ret;	
	}

	var tableBodyCtx = ["tbody", {'id': ids['taskTableBody']},
		// Default value
		['tr',
			['td', {'colspan':6, 'class': 'text-center'},
				"Invalid task ID"
			]
		]		
    ];

	var tableHeadingsCtx = ["thead",
	    ["tr",
	        ['th', "ID:"],
	        ['th', "File Path:"],
	        ['th', "Machine:"],	        
	        ['th', "Score:"],
	        ['th', "Status:"],
	        ['th', "Resubmited"],
	        ['th', "Previous Task"],
	        ['th', "Actions:"]	// (Expand show Installed choco packages, reg keys added)
	    ]
	];

	var tableCtx = ["table", {"class": "table table-bordered table-hover"},
       	tableHeadingsCtx,
        tableBodyCtx        
    ];
	
    var tableCardHeaderCtx = ["div", {"class": "card-header"},
    	['b', "Task Details"]
    ]
    	
    var resubmitBtnCtx = ["button", {'id': ids['taskResubmitTask'], "class": "btn btn-warning"}, "Resubmit"]
    
    var utilsRowCtx = ['div', {'class': "card-header py-1 bg-white text-right"},
			resubmitBtnCtx
	    ];

    var tableCardCtx = ["div", {"class": "card"},
        tableCardHeaderCtx,
        utilsRowCtx,
         	

        ["div", {"class": "card-body", "style": "overflow-x:auto;"},
        	// Table
        	tableCtx
        ]
    ];

    var capeIframeCtx = ["div", {"class": "embed-responsive embed-responsive-16by9"},
	    ["iframe", {'id': ids['taskCapeIframe'], "class": "embed-responsive-item", "src": ""}]
	];

	self.bodyCtx = ["div", {"class": "pt-2"},
	    ["div", {"class": "col-12"},
			tableCardCtx
		],
		capeIframeCtx

	];

	self.setTaskTableData = function(taskData) {
		console.log("taskData", taskData);

		if (!taskData) {
			console.log("taskData Error");
			return 
		}

		var data = genTableRowCtx(taskData);
		console.log("data", data);

		if (!data) {
			console.log("Error no data");
			return;
		}

		$('#'+ids['taskTableBody']).html(
				HTML(data)
			)
		console.log("Successfully updated task table data")

	}

	self.loadIframe = function(taskId) {
		$('#'+ids['taskCapeIframe']).attr('src', baseCapeAnalysisUrl+taskId+'/');
	}

	var loadTaskDetails = function() {
		if (data['taskGetId'] != '') {
			console.log("window.needsUpdate.taskLoadTaskData = true", window.needsUpdate.taskLoadTaskData = true);
			window.needsUpdate.taskLoadTaskData = true;			
		}
	}

	var addEvents = function() {
		$('.'+eleClass['taskActionBtn']).click(function(){
			// Set task arrtribute to not be evaluated
		});

		$('.'+eleClass['taskPrevTaskBtn']).click(function() {
			data.taskGetId = $(this).text();
			loadTaskDetails();
			console.log("prev btn pressed, loading previous task");
		});

		$("#"+ids['taskResubmitTask']).click(function(){
			console.log("Pressed resubmit task")
			data.taskResubmitId = data.taskTableDetails.id;
			window.needsUpdate.taskForceResubmit = true;
		});

		// $('#'+ids['taskActionCol']).click(function(e) {
		// 	e.stopPropagation();
		// 	// e.preventDefault();
		// })
	};
	
	self.display = function() {
		$('#'+ids['bodyRoot']).html(HTML(self.bodyCtx))
		$('nav .nav-item').removeClass('active');
		$('#'+ids['navTaskItem']).addClass('active');

		loadTaskDetails()

		addEvents();
		
	};

	return self;

})()