$( document ).ready(function() {

	var ViewModel = function() {

		var self = this;

		self.items = ko.observableArray([
		  'Walter White',
		  'Skyler White',
		  'Jesse Pinkman',
		  'Hank Schrader',
		  'Walter White, Jr.',
		  'Marie Schrader',
		  'Saul Goodman',
		  'Gustavo Fring',
		  'Mike Ehrmantraut',
		  'Todd Alquist',
		  'Lydia Rodarte-Quayle'
		]);

		self.counter = 0;

		self.itemCount = ko.computed(function() { 
	    	return self.items().length; 
	  	});
        self.question = ko.computed(function() { 
            return self.items()[self.pageIndex]; 
        });
		self.perPage = ko.observable(1);
	  	self.pageIndex = ko.observable(0);

	  	self.setPageIndex = ko.computed(function(number){
	  		self.pageIndex(number);
	  	})

	  	self.page = ko.computed(function() {
    		var startingIndex = self.pageIndex() * self.perPage();
    		return self.items.slice(startingIndex, startingIndex + self.perPage());
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
		    self.itemCount()/self.perPage()) - 1;
		});

		self.pages = ko.computed(function() {
			var indices = [], max = Math.ceil(self.itemCount()/self.perPage());
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