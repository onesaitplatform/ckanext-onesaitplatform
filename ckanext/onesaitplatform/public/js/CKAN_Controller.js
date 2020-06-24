// CKAN ACTIVITY CONTROLLER --------------------------------------------------------------------
var CKAN_Controller = function(){
    
	// DEFAULT PARAMETERS, VAR, CONSTS. 
    var APPNAME = 'onesait Platform ckan Frontend'; 
	var LIB_TITLE = 'Ckan onesait Controller';	
    var logControl = 1;
	
	// ANIMATED COUNTERS
    var animateCounter = function(id,css){
	
		let domElements = id ? '#'+ id : css ? '.' + css : '.count';
		
		$(domElements).each(function () {
			$(this).prop('Counter',0).animate({
				Counter: $(this).text().replace(/[^0-9]/gi, '')
			}, {
				duration: 2000,
				easing: 'swing',
				step: function (now) {
					$(this).text(Math.ceil(now));
				},
				complete: function(){              
					let prefix   = $(this).data('prefix')   ? $(this).data('prefix')   : '';
					let sufix	 = $(this).data('sufix')    ? ' ' + $(this).data('sufix')    : '';
					let positive = $(this).data('positive') ? $(this).data('positive') : ''; 
					let negative = $(this).data('negative') ? $(this).data('negative') : '';

					// apply                            
					$(this).text( positive + '' + negative + '' + prefix + '' + $(this).text() + '' + sufix );               
				}
			})          
		})
	};
	
	// adjust html on 2nd view pages.
	var adjustPages = function(){
		
		var pages = []; // ["organization","group", "showcase", "dataset", "new", "edit"];
		
		var currentPage = window.location.pathname.split("/").pop();
		var found = jQuery.inArray( currentPage, pages ) === -1 ? false : true;
		
		if ( found ){
			
			// apply adjust 
			$('aside.secondary').addClass('hide');
			$('div.primary').removeClass (function (index, className) { return (className.match (/\col-\S+/g) || []).join(' ')});
			$('div.primary').addClass('primary col-md-12 col-xs-12');
			logControl ? console.log("\n" + LIB_TITLE + ": adjustPages() found: " + currentPage + " then adjust.") : '';
		}
		
	};
	
	// CONTROLLER PUBLIC FUNCTIONS 
	return{
		
		// LOAD() JSON LOAD FROM TEMPLATE TO CONTROLLER
		load: function(Data) { 			
			logControl ? console.log("\n" +LIB_TITLE + ': load()') : '';
			return CkanReg = Data;
		},		
	
		// INIT() CONTROLLER INIT CALLS
		init: function(){
			logControl ? console.log("\n" +LIB_TITLE + ': init()') : '';
			
			// launch animated counters
			CKAN_Controller.animateCounters('','counter');
			
			// adjust zones
			CKAN_Controller.adjustZones();
			
		},
		animateCounters: function(id,css){
			logControl ? console.log("\n" +LIB_TITLE + ': animateCounters()') : '';	
			animateCounter(id,css);		
		},
		
		adjustZones: function(){
			logControl ? console.log("\n" +LIB_TITLE + ': adjustZones()') : '';	
			adjustPages();
		}
	}
}(); 
// AUTO INIT CONTROLLER WHEN READY
//jQuery(document).ready(function() {
        
    // AUTO INIT CONTROLLER.
    //CKAN_Controller.init(); 
//});