
$(function(){

	
	$('body').html(HTML(['div', {'id': ids['root'], 'class':'container-fluid'}, 
			layout.nav.ctx,

			['div', {'id': ids['bodyRoot'], 'class': 'container-fluid'}],

			layout.footer().ctx
		]
	));

	HTML.route("home/", layout.home.display);
	HTML.route("task/", layout.task.display);
	HTML.route("submit/", layout.submit.display);
	HTML.route("machines/", layout.machines.display);
	HTML.route("about/", layout.about.display);


	layout.nav.addEvents();
	$('#'+ids['navHomeItem']).addClass('active');

	layout.home.display();

	

	// layout.task().display();

	console.log("loaded main")

}); 