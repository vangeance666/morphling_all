layout.about = (function() {

	var self = {};
	
	var aboutCardBodyCtx = ["div", {"class": "card-body"},
            ["p",
                "In today’s age of the Internet, sophisticated malwares are becoming dangerously common in all aspects of society. Malware attacks have become commonplace in both corporate and consumer industries. As such, effective malware analysis has become vital in the quest to negate the harmful consequences of a successful malware attack. Sophisticated malware contains evasive techniques, built into its executable code, designed to fool malware analysts and evade modern detection techniques. Current implementations revolve around requiring manual intervention by analysts to find and extract the relevant software packages from the internet and prepare the analysis environment before executing the malware. This results in many hours of trial and error which could have been put to better use for effective research.",
                ["p",
                    "In order to address this concern, our team performed extensive research on modern malwares and came up with the idea of an automatic morphing malware analysis platform. Part of our proposed solution is to come up with a working prototype to implement and demonstrate the effectiveness of our approach. Using virtual machines, we developed a proof of concept environment that emulates and streamlines the actual setup of our platform in a physical environment.",
                    ["p",
                        "Our morphing platform employs the usage of technologies such as CAPEv2 sandbox, FOG server, and Chocolatey to automatically prepare an environment that meets the requirements of the evasive malware at each analysis cycle. Upon completion of the entire analysis process, analysts can be assured that the malicious behavior of the evasive malware would have been successfully captured. Our platform is both practical in its implementation in our proof of concept environment, and is built modular, which leaves room for future works and development.",
                        ["div",
                            ["br"],
                            ["br"],
                            ["figure", {"class": "figure center-block"},
                                ["img", {
                                        "src": "img\\ITP_Team2_Network_Architecture.png",
                                        "class": "figure-img img-fluid rounded center-block",
                                        "alt": "An Automated Morphing Malware Analysis Platform"
                                    }
                                ],
                                ["figcaption", {"class": "figure-caption text-center"},
                                    "An Automated Morphing Malware Analysis Platform"
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ];

	var aboutCardTitleCtx = ["div", {"class": "card-header"}, ["h3", "About This Project"]];

	self.bodyCtx = ["div", {"class": "col-12"},
    	["div", {"class": "card"},
    		aboutCardTitleCtx,
    		aboutCardBodyCtx
    	]
	]



	self.display = function() {
		$('#'+ids['bodyRoot']).html(HTML(self.bodyCtx))
		$('nav .nav-item').removeClass('active');
		$('#'+ids['navAboutItem']).addClass('active');
		addEvents();
	}

	return self;	
})();