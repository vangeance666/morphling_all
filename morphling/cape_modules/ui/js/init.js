
var layout = {};

var baseCapeAnalysisUrl = "http://127.0.0.1:8000/analysis/"

var eleClass = {
	navBtn: "nav-btn",
	taskActionBtn: 'task-action-btn', taskPrevTaskBtn: 'task-prev-task-btn',

	homeTaskIdLink: "home-task-id-link"
}

var ids = {
	root: "root",
	bodyRoot: "body-root",

	titleLabel: "title-label",

	navHomeItem: "nav-home-item",
	navTaskItem: "nav-task-item",
	navSubmitItem: "nav-submit-item",
	navMachinesItem: "nav-machine-item",
	navAboutItem: "nav-about-item",

	submitUploadInput: "home-upload-input",
	submitUploadInputLabel: "home-upload-input-label",
	submitUploadBtn: 'home-submit-btn',
	submitMachineSelect: 'submit-machine-select',

	// homeSubmissionTable: "home-submission-table",
	homeTableBody: "home-table-body",
	homeSubmissionRefreshBtn: "home-submission-refresh-btn",


	taskTableBody: "task-table-body",
	taskActionCol: "task-action-col",
	taskCapeIframe: "task-cape-iframe",
	taskResubmitTask: 'task-resubmit-task',

	machinesTableBody: 'machines-table-body',
	machinesStatusRefreshBtn: 'machines-status-refresh-btn'	
};

var tuningOptions = {
	label: 'Misc',
	data: [
		{name: 'Dont re-tune', value: 1}	
	]
}
// var taskSubmitOptions = [
	
// ]

var data = {
	submitSamplePath: '',
	homeSubmissionsData: [],

	taskTableDetails: '', taskGetId: '', taskResubmitId: '',

	machineNames: [], chosenMachine: '', 
	machinesTableData: []
}

window.needsUpdate = {
	submitPromptFile:false, submitSendFile:false, getMachineNames:false,
	homeRetrieveSubmissions:false,

	taskLoadTaskData:false, taskDisableResubmission: false, taskEnableResubmission: false,
	taskForceResubmit:false,

	machinesRetrieveData:false
}


console.log("init.js");


toastr.options = {
	  
	  "debug": false,
	  "newestOnTop": false,
	  "progressBar": false,
	  "positionClass": "toast-top-right",
	  "preventDuplicates": false,
	  "onclick": null,
	  "showDuration": "200",
	  "hideDuration": "1000",
	  "timeOut": "3000",
	  "extendedTimeOut": "1000",
	  "showEasing": "swing",
	  "hideEasing": "linear",
	  "showMethod": "fadeIn",
	  "hideMethod": "fadeOut",
	  "preventDuplicates": true
};


showSuccess = function(s, title) {
	if (title) {
		toastr.success(s, title);
	}
	else {
		toastr.success(s);
	}
}


showInfo = function(t){ 
	toastr.info(t);
}

showLoader = function(t) {
  // $('#refresh').addClass('disabled');
  $.LoadingOverlay('show', {
    image: '',
    custom: $(HTML(['div', {id: 'loader-animation', class: 'row noselect justify-content-center d-flex'},
      ['img', {class: ''}, {src: 'resources/loader.gif'}],
      ['span', {class: ' h4 col-12 ml-2 text-center '}, t]
    ]))
  });
}

showError = function(e) {
	console.log("e is:"+e);
	if (e != '') {
		toastr.error(e);
	}
}

hideLoader = function(error) {
  if (error) toastr.error(error);
  $('#refresh').removeClass('disabled');
  $.LoadingOverlay('hide');
}

