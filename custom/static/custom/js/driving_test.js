/* global $ */
/* global ko */
/* global Howl */
/* global moment */
$( document ).ready(function() {

	var choice_question = new Object();

	var audio_cache = {};
	var audio_play_token = 0;

	var stopAllAudio = function(){
		for (var url in audio_cache) {
			if (audio_cache.hasOwnProperty(url) && audio_cache[url].state() === 'loaded') {
				audio_cache[url].stop();
			}
		}
	}

	var playAudioUrl = function(url){
		if (!url) return;
		var token = ++audio_play_token;
		stopAllAudio();
		if (!audio_cache[url]) {
			audio_cache[url] = new Howl({ src: [url] });
		}
		var sound = audio_cache[url];
		if (sound.state() === 'loaded') {
			sound.play();
		} else {
			sound.once('load', function(){
				if (token === audio_play_token) sound.play();
			});
		}
	}

	var Choice = function(choice_data){
		this.id = choice_data.id;
		this.description = choice_data.description;
		this.audio_url = choice_data.audio_url;
		this.image_url = choice_data.image_url;
		this.video_url = choice_data.video_url;
		
		this.playAudio = function(){
			playAudioUrl(this.audio_url);
		}
	}

	var Question = function(question) {
		this.id  = question.id || null;
		this.human_readable_question_no = question.human_readable_question_no || 0;
		this.exam_question_id = question.eqId;
	    this.question_description = question.question_description;
	    this.choices = ko.observableArray([]);
	    this.selected_choices = ko.observableArray();
	    this.question_type = question.question_type;
	    this.text_entry = ko.observable(question.text_entry || '');
	    this.audio_url = question.audio_url || null;
	    this.image_url = question.image_url || null;
	    this.video_url = question.video_url || null;
	    this.responseStatus = ko.observable(question.responded_to_question || "btn-default");
	    //08093448596 Comfort
	    this.addQuestionOptions = function(choice) {
	        this.choices.push(choice);
	    }.bind(this);

	    this.selected_choices.subscribe(function(selection){
	    	if (selection.constructor == Array) {
				// checkbox
	    		if (selection.length > 0) {
					var current_option = $('.selected');
					current_option.removeClass('selected');
	    			$('#' + choice_question[selection[0]]).removeClass('btn-info');
					$('#' + choice_question[selection[0]]).addClass('btn-primary');
					$('#' + selection[0]).parent().parent().parent().addClass('selected');
	    		}else{
	    			// $('#' + choice_question[selection[0]]).removeClass('btn-info');
	    			// $('#' + choice_question[selection[0]]).addClass('btn-default')
	    			console.log(selection);
	    		}
	    	}else{
				// radio
				var current_option = $('.selected');
				current_option.removeClass('selected');
				$('#' + selection).parent().parent().parent().addClass('selected');
	    		$('#' + choice_question[selection]).removeClass('btn-info');
	    		$('#' + choice_question[selection]).addClass('btn-primary');
	    	}
	    	// var responded = false;
	    	// if(this.question_type < 2){
	    	// 	if (this.selected_choices().length > 0) responded = true;
	    	// }else{
	    	// 	if(this.text_entry() && this.text_entry().length > 0) {
	    	// 		responded = true;
	    	// 	}
	    	// }
	    	// if(responded) this.responseStatus("btn-success");
	    	// return responded;
	    });
	}

	var ViewModel = function() {

		var self = this;

		self.questions = ko.observableArray([]);
		self.started = ko.observable(false);
		self.countdown_to_start_test;
		self.countdown_to_finish_test;
		self.countdown_date;
		self.duration = '00:00:00';
		self.exam_language = 'en';

		self.populateExamInfo = function(examInfo){
			self.exam_language = examInfo.exam_preferred_language ? examInfo.exam_preferred_language : 'en';
			self.countdown_to_start_test = examInfo.preffered_date_and_time_of_test;
		};
		
		self.populateModelOld = function(questionSet){
			self.duration = questionSet[0].exam.duration;//TODO separate exam fom question
			// console.log(self)
			var mSchedule = moment(questionSet[0].exam.start_date_if_sheduled)
				.clone()
				.add(moment.duration(self.duration));
				// console.log(mSchedule)
			self.countdown_date= mSchedule.toDate();
			questionSet = _.shuffle(questionSet);
			for (var i = 0; i < questionSet.length; i++){
				self.addQuestion(questionSet[i].question, questionSet[i].id, 'Q' + (i + 1));
			}
			self.start(moment.duration(self.duration).asSeconds());
		};
		
		self.populateModel = function(questionSet){
			qs = questionSet.questions;
			self.duration = questionSet.exam.duration;//TODO separate exam fom question
			self.countdown_to_start_test = questionSet.exam.start_date_if_sheduled;
			self.countdown_to_finish_test = moment()
				.clone()
				.add(moment.duration(self.duration));
			console.log(self.questions);
			questionSet = _.shuffle(qs);
			for (var i = 0; i < questionSet.length; i++){
				self.addQuestion(questionSet[i], questionSet[i].id, 'Q' + (i + 1), self.exam_language);
			}
			// self.start();
			self.start(moment.duration(self.duration).asSeconds());
		};


		self.showFinishTestLoader = function(){
			var modal = $('.js-loading-bar'),
			// var modal = $('.js-loading-bar').modal({backdrop: 'static', keyboard: false}),
      		bar = modal.find('.progress-bar');
      		modal.modal('show');
      		bar.addClass('animate');
		}

		self.finishTest = function() {
			self.showFinishTestLoader();
		  	// Finish Test
		  	var answerSet = $.map(self.questions(), function(question) {
		  		var choice_selected = [];
		  		if(question.question_type == 0 && question.selected_choices().length > 0){
		  			choice_selected.push(question.selected_choices());
		  		}
		  		if(question.question_type == 1 && question.selected_choices().length > 0){
		  			choice_selected = question.selected_choices();
		  		}
            	return {
	                question_id: question.id,
	                exam_question_id: question.exam_question_id,
	                question_type: question.question_type == 0 ? 'scqt' : (question.question_type == 1 ? 'mcqt' : 'tet'),
	                text_entry: question.text_entry(),
	                selected_choice_ids: choice_selected,
            	};
        	});
        	// console.log(answerSet);
        	self.processExam(answerSet);
		};


		self.audioQuestionPlay = function(){
			playAudioUrl(self.questions()[self.pageIndex()].audio_url);
		}

		self.processExam = function(answerSet){
			var request = JSON.stringify(answerSet);
		    // $('#loader').dimmer('show');
		    // setTimeout(function() {
		    $.ajax({
		        url: "/ap/process_candidate_exam", 
		        method: 'POST',
		        data: request,
		        dataType: 'json',
		        contentType: 'application/json',
		        statusCode: {
				    201: function() {
				      window.location = '/ap/candidate_result'
				    },
				    200: function() {
				      window.location = '/ap/candidate_result'
				    },
				  }
		    }).done(function( data ) {
		        // $('#loader').dimmer('hide');
		        // console.log(data);
		    });
		  // }, 0);
		}

		self.start = function(duration){
			self.pageIndex(0);
			// $('#countdown').data('timer', duration);
			// $("#countdown").TimeCircles({start: true, animation: "smooth"}); 
			var clock = $('#countdown').FlipClock(duration, {
				clockFace: 'HourCounter',
		        autoStart: true,
				countdown: true,
		        callbacks: {
		        	stop: function() {
		        		self.finishTest()
		        	}
		        }
			});
			self.started(true);
			// start_video_for_video();
		}

		self.end = function(){
			//TODO
		}

		self.addQuestionOld = function(question, eqId, qNo) {
			var mQuestion = new Question({
				id: question.id,
				eqId: eqId,
				human_readable_question_no: qNo,
	        	question_description: question.question,
	        	question_type: question.question_type == 'scqt' ? 0 : 
	        		(question.question_type == 'mcqt' ? 1 : 2),
	        	image_url: question.image,
			    audio_url: question.audio,
			    video_url: question.video,
			    display_language: question.language,
	        	// responded_to_question: false,
			})
			for (var i = 0;  (mQuestion.question_type != 2 && 
				i < question.answer_choices.length); i++){
				mQuestion.addQuestionOptions(new Choice({
			    	id: question.answer_choices[i].id,
			    	description: question.answer_choices[i].question_option,
			    	image_url: question.answer_choices[i].image,
			    	audio_url: question.answer_choices[i].audio,
			    	video_url: question.answer_choices[i].video,
			    	display_language: question.answer_choices[i].language,
			    	// selected: false,
			    }));
				choice_question[question.answer_choices[i].id] = question.id; //hashmap
			}
    		self.questions.push(mQuestion);
	    };
	    
	    self.addQuestion = function(question, eqId, qNo, lang) {
			var tQuestion = '';
			var tImage = null;
			var tAudio = null;
			var tVideo = null;
			if (lang == "en") {
				tQuestion = question.question;
				tImage = question.image;
				tAudio = question.audio;
				tVideo = question.video;
			}else{
				for (var i = 0; i < question.translated_questions.length; i++){
					if (question.translated_questions[i].language == lang) {
						tQuestion = question.translated_questions[i].translated_question;
						tImage = question.translated_questions[i].image == null ? question.image : 
						question.translated_questions[i].image;
						tAudio = question.translated_questions[i].audio == null ? question.audio : 
						question.translated_questions[i].audio;
						tVideo = question.translated_questions[i].video == null ? question.video : 
						question.translated_questions[i].video;
						break;
					}
				}
			}

			var mQuestion = new Question({
				id: question.id,
				eqId: eqId,
				human_readable_question_no: qNo,
	        	question_description: tQuestion != '' ? tQuestion : question.question,
	        	question_type: question.question_type == 'scqt' ? 0 : 
	        		(question.question_type == 'mcqt' ? 1 : 2),
	        	image_url: tImage != null ? tImage : question.image,
			    audio_url: tAudio != null ? tAudio : question.audio,
			    video_url: tVideo != null ? tVideo : question.video,
			    display_language: question.language,
	        	// responded_to_question: false,
			});
			var tCounter = 0; //number of option added to question so far.
			for (var i = 0;  (mQuestion.question_type != 2 && 
				i < question.answer_choices.length); i++){
				var tChoice = '';
				var tChoiceImage = null;
				var tChoiceAudio = null;
				var tChoiceVideo = null;
				if (lang == "en") {
					tChoice = question.answer_choices[i].question_option;
					tChoiceImage = question.answer_choices[i].image;
					tChoiceAudio = question.answer_choices[i].audio;
					tChoiceVideo = question.answer_choices[i].video;
				}else{
					var tFound = 0; //number of options found so far.
					for (var w = 0; w < question.translated_questions.length; w++){
						if(question.translated_questions[w].language != lang ) continue;
						for (var j = 0; j < question.translated_questions[w].translated_question_answer_choices.length; j++){
							if (question.translated_questions[w].translated_question_answer_choices[j].language == lang) {
								tFound++;
								if (tFound > tCounter) {
									tChoice = question.translated_questions[w].translated_question_answer_choices[j].translated_question_option;
									tChoiceImage = question.translated_questions[w].translated_question_answer_choices[j].image == null ? 
									question.translated_questions[w].image : 
									question.translated_questions[w].translated_question_answer_choices[j].image;
									tChoiceAudio = question.translated_questions[w].translated_question_answer_choices[j].audio == null ? 
									question.translated_questions[w].audio : 
									question.translated_questions[w].translated_question_answer_choices[j].audio;
									tChoiceVideo = question.translated_questions[w].translated_question_answer_choices[j].video == null ? 
									question.translated_questions[w].video : 
									question.translated_questions[w].translated_question_answer_choices[j].video;
									tCounter++;
									break;
								}
							}
						}
					}
				}
				mQuestion.addQuestionOptions(new Choice({
			    	id: question.answer_choices[i].id,
			    	description: tChoice != '' ? tChoice : question.answer_choices[i].question_option,
			    	image_url: tChoiceImage != null ? tChoiceImage : question.answer_choices[i].image,
			    	audio_url: tChoiceAudio != null ? tChoiceAudio : question.answer_choices[i].audio,
			    	video_url: tChoiceVideo != null ? tChoiceVideo : question.answer_choices[i].video,
			    	display_language: question.answer_choices[i].language,
			    	// selected: false,
			    }));
				choice_question[question.answer_choices[i].id] = question.id; //hashmap
			}
    		self.questions.push(mQuestion);
	    };

		self.counter = 0;

		self.questionCount = ko.computed(function() { 
	    	return self.questions().length; 
	  	});
		self.perPage = ko.observable(1);
	  	self.pageIndex = ko.observable(0);

	  	self.setPageIndex = function(number){
	  		self.pageIndex(number);
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
	loadUserExamDetails();
	
	function loadUserExamDetails(){
		$.ajax({url: "/ap/load_candidate_exam_info/"})
  		.done(function( examInfo ) {
  			// console.log(questionSet);
  			if (examInfo) {
  				vModel.populateExamInfo(examInfo);
  				loadQuestionSet();
  			}else{
  				alert("Sorry, the questions for this exams have not been set, please contact the admin.");
  			}
  		});
	}

	function loadQuestionSet(){
		$.ajax({url: "/ap/load_candidate_questions/"})
  		.done(function( questionSet ) {
  			if (questionSet.questions && questionSet.questions.length > 0) {
  				if (questionSet.hasOwnProperty("finished")){
  					alert("You have already taken this Exam");
  					window.location.replace('/ap/candidate_result');
  				}
  				else{
					vModel.populateModel(questionSet);
  				}
  			}else{
  				alert("Sorry, the questions for this exams have not been set, please contact the admin.");
  			}
  		});
	}
	
});