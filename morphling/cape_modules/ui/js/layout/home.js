layout.home = (function() {
	
	var self = {}; 

	var genTaskIdsCtx = function(taskIds) {
		ret = [];
		for (var i = 0; i < taskIds.length; ++i) {
			if (taskIds[i] != -1) {
				// ret.push(["a", {'class': 'px-2', "href": "#task?id="+taskIds[i]}, taskIds[i]]);	
				ret.push(["a", {'class': 'pl-2 '+eleClass['homeTaskIdLink'], "href": "#task"}, taskIds[i]]);	
			} else {
				ret.push(["a", {'class': 'pl-2'}, '-']);	
			}
			if (i != taskIds.length-1) {
				ret.push(['a',',']);		
			}
		}
		return ret;
	}
	// later put color
	var genScoresCtx = function(malScores) {
		ret = [];
		for (var i = 0; i < malScores.length; ++i) {
			ret.push(["a", {'class': 'pl-2'}, malScores[i]])
			if (i != malScores.length-1) {
				ret.push(['a',',']);		
			}
		}
		return ret;	
	}

	var genTableRowCtx = function(hash, taskIds, malScores, expandableText) {
		return [
		    ["tr", {"data-widget": "", "aria-expanded": ""},
		        ["td", hash],
		        ["td", genTaskIdsCtx(taskIds)],
		        ["td", genScoresCtx(malScores)]
		    ]
		    // ["tr", {"class": "expandable-body d-none"},
		    //     ["td", {"colspan": "5"}, ["p", expandableText]]
		    // ]
		];
	}

	var tableBodyCtx = ["tbody", {'id': ids['homeTableBody']},
		// Default value
		['tr',
			['td', {'colspan':3, 'class': 'text-center'},
				"No Submissions yet"		
			]
		]		
    ]

	var tableHeadingsCtx = ["thead",
	    ["tr",
	        ["th", "SHA-256 File Hash"],
	        ["th", "Tasks IDs"],
	        ["th", "Scores"]
	    ]
	];

	var tableCtx = ["table", {"class": "table table-bordered table-hover"},
       	tableHeadingsCtx,
        tableBodyCtx        
    ];
	
	var utilRefreshBtnCtx =  ["button", {
	    		"id": ids['homeSubmissionRefreshBtn']	,
	            "class": "home-refresh-button btn btn-md btn-success",
	        },
	        ["span", {"class": "fas fa-sync fa-spin-hover", "aria-hidden": "true"}]
	    ];

    var tableCardHeaderCtx = ["div", {"class": "card-header"},
    	['b', "Summissions"]
    ]

    

    var utilsRowCtx = 
	        ['div', {'class': "card-header text-right py-1 bg-white "},
	        	utilRefreshBtnCtx	    	
		    ]
	    ;

    var tableCardCtx = ["div", {"class": "card"},
	    tableCardHeaderCtx,
	    utilsRowCtx,
        ["div", {"class": "card-body", "style": "overflow-x:auto;"},
        	// Table
        	tableCtx
        ]
    ];


	self.bodyCtx = ["div", {"class": "pt-2"},
	    ["div", {"class": "col-12"},
			tableCardCtx
		]
	]

	self.addTaskIdEvents = function() {
		$('.'+eleClass['homeTaskIdLink']).click(function() {
			data.taskGetId = $(this).text();
			console.log("data.taskGetId", data.taskGetId);			
		});
		console.log("added task id events");
	}

	var addEvents = function() {
		// 1 Button to refresh
		$('#'+ids['homeSubmissionRefreshBtn']).click(function() {
			showInfo('Requested for update of submissions info.');
			window.needsUpdate.homeRetrieveSubmissions = true;
		});

		self.addTaskIdEvents()

		console.log("added homejs events")
	}

	var fillTableWithSubmissions = function() {
		var rowsCtx = []

		console.log("submissiondata got smth");
			for (const submission of data.homeSubmissionsData){

				var taskIds = submission['tasks'].map(item => { 
					if (item.id == null) {
						return "-1";
					}
					return item.id;
				});

				var malScores = submission['tasks'].map(item => { 
					if (item.mal_score == null) {
						return "-1";
					}
					return item.mal_score;
				});

				row = genTableRowCtx(submission['hash'], taskIds, malScores, "HEHE EXPAND TEXT")
				if (row) {
					rowsCtx.push(row);
				}			
			}

		if (rowsCtx) {
			$('#'+ids['homeTableBody']).html(HTML(rowsCtx))
			self.addTaskIdEvents()
		}	

	}

	self.updateSubmissionTable = function() {
		if (data.homeSubmissionsData) {
			fillTableWithSubmissions(data.homeSubmissionsData);
		}		
	}


	self.display = function() {
		$('#'+ids['bodyRoot']).html(HTML(self.bodyCtx))

		$('nav .nav-item').removeClass('active');
		$('#'+ids['navHomeItem']).addClass('active');

		addEvents();

		window.needsUpdate.homeRetrieveSubmissions = true; //Toggle update table
	}

	return self;
})()