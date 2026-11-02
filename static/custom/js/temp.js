		self.questions = ko.observableArray([

		    new Question({
		    	id: 'xxx',
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