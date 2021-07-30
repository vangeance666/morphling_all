layout.machines = (function () {
	var self = {};

	var genTableRowCtx = function(name, status, taskId) {
		return [
		    ["tr", {"data-widget": "expandable-table", "aria-expanded": "false"},
		        ["td", name],
		        ["td", status],
		        ["td", taskId]
		    ]
		    // ["tr", {"class": "expandable-body d-none"},
		    //     ["td", {"colspan": "5"}, ["p", expandableText]]
		    // ]
		];
	}

	var tableBodyCtx = ["tbody", {'id': ids['machinesTableBody']},
		// Default value
		['tr',
			['td', {'colspan':3, 'class': 'text-center'},
				"No machines yet"		
			]
		]		
    ]

	var tableHeadingsCtx = ["thead",
	    ["tr",
	        ["th", "Name"],
	        ["th", "Status"],
	        ["th", "Allocated Task" ]
	    ]
	];

	var tableCtx = ["table", {"class": "table table-bordered table-hover"},
       	tableHeadingsCtx,
        tableBodyCtx        
    ];
	
    var tableCardHeaderCtx = ["div", {"class": "card-header"},
        ['b', "Machines Status"]
    ]

    var utilRefreshBtnCtx =  ["button", {"id": ids['machinesStatusRefreshBtn'],        	
                "type": "button",
                "class": "btn btn-secondary",
                "title": "Refresh Table"
            }, ["span", {"class": "fas fa-sync fa-spin-hover", "aria-hidden": "true"}]
        ];


    var utilsRowCtx = ['div', {'class': "card-header text-right py-1 bg-white "},
			utilRefreshBtnCtx	    	
		];

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
	];

	var addEvents = function () {
		$('#'+ids['machinesStatusRefreshBtn']).click(function(){
			showInfo('Requested for update of machines status');
			window.needsUpdate.machinesRetrieveData = true;
		});


	}

	var updateMachinesTableEx = function() {
		var rowsCtx = []

		for (const machine of data.machinesTableData){
			// data['label'], data['status'], data['allocated_task'] #Null if NOne else 'id' key
			var rowTaskId = "None"
			
			console.log("rowTaskId", rowTaskId);

			if (machine['allocated_task'] != null) {
				rowTaskId = machine['allocated_task']['id'];
			}

			console.log("rowTaskId", rowTaskId);

			row = genTableRowCtx(machine['label'], machine['status'], rowTaskId)

			if (row) {
				rowsCtx.push(row);
			}			
		}

		console.log("rowsCtx", rowsCtx);

		if (rowsCtx.length) {
			$('#'+ids['machinesTableBody']).html(HTML(rowsCtx))
		}
		console.log("Finished updateMachinesTable")

	}

	self.updateMachinesTable = function() {
		if (data.machinesTableData) {
			console.log("Updating machines table")
			updateMachinesTableEx(data.machinesTableData);
		}else {
			console.log("Not Updating machines table")
		}
	}


	self.display = function() {
		$('#'+ids['bodyRoot']).html(HTML(self.bodyCtx))

		$('nav .nav-item').removeClass('active');
		$('#'+ids['navMachinesItem']).addClass('active');

		addEvents();
		// self.updateMachinesTable();

		window.needsUpdate.machinesRetrieveData = true; //Toggle update table

	}


	return self;

})();