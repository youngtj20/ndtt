$( document ).ready(function() {

	function loadCandidateData(){
		$.ajax({
	        url: "/ap/get_candidate_data", 
	        method: 'GET',
	        // data: request,
	        // dataType: 'json',
	        // contentType: 'application/json',
	    }).done(function( data ) {
	        $('#loader').dimmer('hide');
	        if(data.status){

	        }else{
	            alert('An error occured');
	        }
	    });
	}

	var Choice = function(choice_data){
		self = this;
		self.id = choice_data.id;
		self.description = choice_data.description;
		self.audio_url = choice_data.audio_url;
		self.image_url = choice_data.image_url;
		self.video_url = choice_data.video_url;
		self.selected = choice_data.selected || false;
	}

	var Question = function(question, choices) {
		self = this;
	    self.question_description = question.question_description;
	    self.choices = ko.observableArray(choices);
	    self.question_type = question.question_type;
	    self.text_entry = ko.observable(question.text_entry || '');
	    self.responded_to_question = ko.observable(question.responded_to_question || false);

	    self.hasResponded = ko.computed(function(){
	    	var responded = false;
	    	if(self.question_type < 2){
	    		for (var i = 0; i < self.choices().length; i++) {
		    		if(self.choices()[i].selected){
		    			responded = true;
		    			break;
		    		}
		    	};
	    	}else{
	    		if(self.text_entry() && self.text_entry().length > 0) {
	    			responded = true;
	    		}
	    	}
	    	if(responded) responded_to_question = true;
	    	return responded;
	    })

	    self.responseStatus = ko.computed(function() {
        	return !self.hasResponded() ? "btn-default" : "btn-info";
    	});

	    //08093448596 Comfort
	 
	    self.addChoice = function(choice) {
	        self.choices.push(choice);
	    }.bind(self);
	}

	var ViewModel = function() {

		var self = this;

		self.questions = ko.observableArray([]),

		self.counter = 0;

		self.questionCount = ko.computed(function() { 
	    	return self.questions().length; 
	  	});
		self.perPage = ko.observable(1);
	  	self.pageIndex = ko.observable(0);

	  	self.setPageIndex = function(number){
	  		if(number) {
	  			self.pageIndex(number);
	  		}else{
	  			self.pageIndex(0);
	  		}
	  	};

	  	self.page = ko.computed(function() {
    		var startingIndex = self.pageIndex() * self.perPage();
    		return self.questions().slice(startingIndex, startingIndex + self.perPage());
		});

		self.atFirstPage = ko.computed(function() {
	  		return self.pageIndex() === 0;
		});

		self.previousPage = function() {
		  if (!self.atFirstPage()) {
		    self.pageIndex(self.pageIndex() - 1);
		  }
		};

		self.nextPage = function() {
		  if (!self.atLastPage()) {
		    self.pageIndex(self.pageIndex() + 1);
		  }
		};

		self.atLastPage = ko.computed(function() {
		  return self.pageIndex() === Math.ceil(
		    self.questionCount()/self.perPage()) - 1;
		});

		self.pages = ko.computed(function() {
			var indices = [], max = Math.ceil(self.questionCount()/self.perPage());
		  	for (var i = 0; i < max; i++) {
		    	indices.push({
		      	label: i + 1,
		      	isCurrentPage: self.pageIndex() === i,
		      	handler: self.pageIndex.bind(self, i)
		    });
		  }
		  return indices;
		});
	};

	var vModel = new ViewModel();
	ko.applyBindings(vModel);
});