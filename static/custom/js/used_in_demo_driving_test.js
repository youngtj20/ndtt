$( document ).ready(function() {

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
		self.id  = question.id || null;
	    self.question_description = question.question_description;
	    self.choices = ko.observableArray(choices);
	    self.question_type = question.question_type;
	    self.text_entry = ko.observable(question.text_entry || '');
	    self.audio_url = question.audio_url || null;
	    self.image_url = question.image_url || null;
	    self.video_url = question.video_url || null;
	    self.responded_to_question = ko.observable(question.responded_to_question || false);

	    self.hasResponded = function(){
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
	    	if(responded) self.responded_to_question(true);
	    	return responded;
	    }

	    self.responseStatus = ko.computed(function() {
	    	if (self.responded_to_question()) {
	    		return "btn-info";
	    	}
        	return !self.hasResponded()  ? "btn-default" : "btn-info";
    	});

	    //08093448596 Comfort
	 
	    self.addChoice = function(choice) {
	        self.choices.push(choice);
	    }.bind(self);
	}

	var ViewModel = function() {

		var self = this;

		self.questions = ko.observableArray([
	        new Question({
	        	question_description: "When turning your motorcycle in the road you must",
	        	question_type: 0, //single-choice
	        	responded_to_question: false,
	    	}, [
		    	new Choice({
		    		id: '1xx',
		    		description: "Use only the mirrors",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false, //1xx
		    	}),
		    	new Choice({
		    		id: '2xx',
		    		description: "Use an available driveway",
		    		image_url:'',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//2xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Overhang the kerb",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Check all around",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	})
		    ]),


		    new Question({
	        	question_description: "You should not use a mobile phone whilst riding",
	        	question_type: 0, //single-choice
	        	responded_to_question: false,
	    	}, [
		    	new Choice({
		    		id: '1xx',
		    		description: "Because the reception is poor when the engine is running",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false, //1xx
		    	}),
		    	new Choice({
		    		id: '2xx',
		    		description: "Because it might distract your attention from the road ahead",
		    		image_url:'',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//2xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Because you may be fined for doing so",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Because you can loose your phone while riding",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	})
		    ]),


		    new Question({
	        	question_description: "Your motorcycle is fitted with a hands-free phone system, This could.",
	        	question_type: 0, //single-choice
	        	responded_to_question: false,
	    	}, [
		    	new Choice({
		    		id: '1xx',
		    		description: "Be very good for road safety",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false, //1xx
		    	}),
		    	new Choice({
		    		id: '2xx',
		    		description: "Help you in planning the route ahead",
		    		image_url:'',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//2xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Distract your attention from the road",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Be quite safe as long as you slow down",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	})
		    ]),


		    new Question({
	        	question_description: "Using a hands-free phone is likely to",
	        	question_type: 0, //single-choice
	        	responded_to_question: false,
	    	}, [
		    	new Choice({
		    		id: '1xx',
		    		description: "Use only the mirrors",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false, //1xx
		    	}),
		    	new Choice({
		    		id: '2xx',
		    		description: "Use an available driveway",
		    		image_url:'',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//2xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Overhang the kerb",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Check all around",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	})
		    ]),


		    new Question({
	        	question_description: "Riding the motorcycle when you are feeling cold, could cause you to",
	        	question_type: 0, //single-choice
	        	responded_to_question: false,
	    	}, [
		    	new Choice({
		    		id: '1xx',
		    		description: "Be more alert",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false, //1xx
		    	}),
		    	new Choice({
		    		id: '2xx',
		    		description: "Be more relaxed",
		    		image_url:'',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//2xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "React more quickly",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Lose concentration",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	})
		    ]),


		    new Question({
	        	question_description: "The black arrow in the diagram means that you should not plan to",
	        	question_type: 0, //single-choice
	        	responded_to_question: false,
	        	image_url: '/static/custom/images/turnleft.jpg',
	    	}, [
		    	new Choice({
		    		id: '1xx',
		    		description: "Turn left",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false, //1xx
		    	}),
		    	new Choice({
		    		id: '2xx',
		    		description: "Turn right",
		    		image_url:'',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//2xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Overtake",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Slow down",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	})
		    ]),


		    new Question({
	        	question_description: "When turning your motorcycle in the road you must",
	        	question_type: 0, //single-choice
	        	responded_to_question: false,
	    	}, [
		    	new Choice({
		    		id: '1xx',
		    		description: "Use only the mirrors",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false, //1xx
		    	}),
		    	new Choice({
		    		id: '2xx',
		    		description: "Use an available driveway",
		    		image_url:'',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//2xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Overhang the kerb",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Check all around",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	})
		    ]),


		    new Question({
	        	question_description: "When turning your motorcycle in the road you must",
	        	question_type: 0, //single-choice
	        	responded_to_question: false,
	    	}, [
		    	new Choice({
		    		id: '1xx',
		    		description: "Use only the mirrors",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false, //1xx
		    	}),
		    	new Choice({
		    		id: '2xx',
		    		description: "Use an available driveway",
		    		image_url:'',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//2xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Overhang the kerb",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Check all around",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	})
		    ]),


		    new Question({
	        	question_description: "When turning your motorcycle in the road you must",
	        	question_type: 0, //single-choice
	        	responded_to_question: false,
	    	}, [
		    	new Choice({
		    		id: '1xx',
		    		description: "Use only the mirrors",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false, //1xx
		    	}),
		    	new Choice({
		    		id: '2xx',
		    		description: "Use an available driveway",
		    		image_url:'',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//2xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Overhang the kerb",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Check all around",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	})
		    ]),

		    new Question({
	        	question_description: "When turning your motorcycle in the road you must",
	        	question_type: 0, //single-choice
	        	responded_to_question: false,
	    	}, [
		    	new Choice({
		    		id: '1xx',
		    		description: "Use only the mirrors",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false, //1xx
		    	}),
		    	new Choice({
		    		id: '2xx',
		    		description: "Use an available driveway",
		    		image_url:'',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//2xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Overhang the kerb",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Check all around",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	})
		    ]),


		    new Question({
	        	question_description: "When turning your motorcycle in the road you must",
	        	question_type: 0, //single-choice
	        	responded_to_question: false,
	    	}, [
		    	new Choice({
		    		id: '1xx',
		    		description: "Use only the mirrors",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false, //1xx
		    	}),
		    	new Choice({
		    		id: '2xx',
		    		description: "Use an available driveway",
		    		image_url:'',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//2xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Overhang the kerb",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Check all around",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	})
		    ]),


		    new Question({
	        	question_description: "When turning your motorcycle in the road you must",
	        	question_type: 0, //single-choice
	        	responded_to_question: false,
	    	}, [
		    	new Choice({
		    		id: '1xx',
		    		description: "Use only the mirrors",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false, //1xx
		    	}),
		    	new Choice({
		    		id: '2xx',
		    		description: "Use an available driveway",
		    		image_url:'',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//2xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Overhang the kerb",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Check all around",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	})
		    ]),


		    new Question({
	        	question_description: "When turning your motorcycle in the road you must",
	        	question_type: 0, //single-choice
	        	responded_to_question: false,
	    	}, [
		    	new Choice({
		    		id: '1xx',
		    		description: "Use only the mirrors",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false, //1xx
		    	}),
		    	new Choice({
		    		id: '2xx',
		    		description: "Use an available driveway",
		    		image_url:'',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//2xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Overhang the kerb",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Check all around",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	})
		    ]),


		    new Question({
	        	question_description: "When turning your motorcycle in the road you must",
	        	question_type: 0, //single-choice
	        	responded_to_question: false,
	    	}, [
		    	new Choice({
		    		id: '1xx',
		    		description: "Use only the mirrors",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false, //1xx
		    	}),
		    	new Choice({
		    		id: '2xx',
		    		description: "Use an available driveway",
		    		image_url:'',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//2xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Overhang the kerb",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Check all around",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	})
		    ]),


		    new Question({
	        	question_description: "When turning your motorcycle in the road you must",
	        	question_type: 0, //single-choice
	        	responded_to_question: false,
	    	}, [
		    	new Choice({
		    		id: '1xx',
		    		description: "Use only the mirrors",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false, //1xx
		    	}),
		    	new Choice({
		    		id: '2xx',
		    		description: "Use an available driveway",
		    		image_url:'',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//2xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Overhang the kerb",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Check all around",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	})
		    ]),


		    new Question({
	        	question_description: "When turning your motorcycle in the road you must",
	        	question_type: 0, //single-choice
	        	responded_to_question: false,
	    	}, [
		    	new Choice({
		    		id: '1xx',
		    		description: "Use only the mirrors",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false, //1xx
		    	}),
		    	new Choice({
		    		id: '2xx',
		    		description: "Use an available driveway",
		    		image_url:'',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//2xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Overhang the kerb",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Check all around",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	})
		    ]),


		    new Question({
	        	question_description: "When turning your motorcycle in the road you must",
	        	question_type: 0, //single-choice
	        	responded_to_question: false,
	    	}, [
		    	new Choice({
		    		id: '1xx',
		    		description: "Use only the mirrors",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false, //1xx
		    	}),
		    	new Choice({
		    		id: '2xx',
		    		description: "Use an available driveway",
		    		image_url:'',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//2xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Overhang the kerb",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Check all around",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	})
		    ]),


		    new Question({
	        	question_description: "When turning your motorcycle in the road you must",
	        	question_type: 0, //single-choice
	        	responded_to_question: false,
	    	}, [
		    	new Choice({
		    		id: '1xx',
		    		description: "Use only the mirrors",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false, //1xx
		    	}),
		    	new Choice({
		    		id: '2xx',
		    		description: "Use an available driveway",
		    		image_url:'',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//2xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Overhang the kerb",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Check all around",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	})
		    ]),


		    new Question({
	        	question_description: "When turning your motorcycle in the road you must",
	        	question_type: 0, //single-choice
	        	responded_to_question: false,
	    	}, [
		    	new Choice({
		    		id: '1xx',
		    		description: "Use only the mirrors",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false, //1xx
		    	}),
		    	new Choice({
		    		id: '2xx',
		    		description: "Use an available driveway",
		    		image_url:'',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//2xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Overhang the kerb",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Check all around",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	})
		    ]),


		    new Question({
	        	question_description: "When turning your motorcycle in the road you must",
	        	question_type: 0, //single-choice
	        	responded_to_question: false,
	    	}, [
		    	new Choice({
		    		id: '1xx',
		    		description: "Use only the mirrors",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false, //1xx
		    	}),
		    	new Choice({
		    		id: '2xx',
		    		description: "Use an available driveway",
		    		image_url:'',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//2xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Overhang the kerb",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	}),
		    	new Choice({
		    		id: '3xx',
		    		description: "Check all around",
		    		image_url: '',
		    		audio_url: '',
		    		video_url: '',
		    		selected: false,//3xx
		    	})
		    ]),

       	]);

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