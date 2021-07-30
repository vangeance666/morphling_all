layout.footer = function () {
	
	self.ctx = ["footer", {"class": "text-center text-lg-start fixed-bottom"},
	["br"],
    ["div", {
            "class": "text-center p-3 bg-light",
        },
        "© 2021 Copyright",
        ["a", {"class": "text-dark", "href": "https://www.singaporetech.edu.sg/"},
		["br"],
            "An Industry Integrated Team Project: Malware Analysis - An Investigation on Malware Trigger Conditions. By Students of SIT"
        ]
    ]
];

	return self;
};