layout.nav = (function() {
	
	var self = {};

	var genBtnCtx = function(id, classValues, label, hrefLink) {
		return ["li", {'id': id, "class": "nav-item cursor-pointer" + eleClass['navBtn']},
	        ["a", {"class": "nav-link", 'href': hrefLink},
	            ["span", {"class": "mr-2 " + classValues}],
	            label
	        ]
	    ];
	}

	self.ctx = ["nav", {"class": "navbar navbar-expand-sm navbar-light bg-light position-relative py-0"},
	    ["div", {"class": "collapse navbar-collapse"},
	        ["a", {
	                "class": "nav-link",
	                "style": "padding-right:20px;padding-left:10px",
	            },
	            ["img", {"src": "img/logo.png"}]
	        ],
	        ["ul", {"class": "navbar-nav mr-auto"},
	            genBtnCtx(ids['navHomeItem'], "fas fa-tachometer-alt", "Home", "#home"),
				genBtnCtx(ids['navTaskItem'], "fas fa-tasks", "Task\tDetails", "#task"),
				genBtnCtx(ids['navMachinesItem'], "fas fa-laptop-code", "Machines", "#machines"),
				genBtnCtx(ids['navSubmitItem'], "fas fa-file", "Submit", "#submit"),
				
	        ],
	        ['ul', {'class': 'navbar-nav ml-auto'},
	        	genBtnCtx(ids['navAboutItem'], "fas fa-info-circle", "About", "#about")
	        ]

	    ]
	];

	self.addEvents = function() {
		// 1 Each button to toggle different view
		// 2 Ensure that clicking each button will also highlight the button
		$('.'+eleClass['navBtn']).click(function(){
			$('.'+eleClass['navBtn']).removeClass("active");
			$(this).addClass("active");
			console.log("Clicked on nav item");

		});

		console.log("nav added events");

	
	}

	return self;

})();