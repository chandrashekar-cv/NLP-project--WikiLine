$('#article_name').change(
	function() {
		//Load the corresponding category names and values	
		//Example json <article_id>.json
		var article_id = $('#article_name').val();
		//article_id = "1";
		$.getJSON( article_id +".json", function(data){
			//console.log($('#article_name').val());
			// console.log(data);
			// console.log(data.categories);
			$.each(data.categories, function(key, value){
				// console.log(value.id);
				// console.log(value.name);
				 $('#article_category')
         			.append($("<option></option>")
         			.attr("value",value.id)
         			.text(value.name));
			});
		});
});


$('#submit').click(function() {
	$('#Wikiline').html("");
	//Read the Article Name
	var article_id = $('#article_name').val();
	if(article_id === "-1"){
		alert("Please select an article");
		return;
	}
	var category_id = $('#article_category').val();
	d3.json("example.json", function(json) {

		if (json === null) return; // parse problem, nothing to do here

		// setup data for chart
		
		
		//strip the json on the number of results
		json.events.sort(function(a,b) { return a.score > b.score ? -1 : a.score < b.score ? 1 : 0; });

		console.log(json.events.length);
		var num_events = Number($('#num_event').val());
		console.log(num_events);
		if(num_events < json.events.length) {
			for(var i=json.events.length-1; i>=num_events; i--){
				json.events.splice(i,1);
				console.log("Splicing!!")
			}
		}
		console.log(json);

		json.events.sort(function(a,b) { return a.date < b.date ? -1 : a.date > b.date ? 1 : 0; });

		json.events.forEach(function(p,i) {
			//p.new = "try";
			//Add image url's here

		});
		// instantiate the chart

		var chart = wikiTimelineChart(); 
		
		chart.date(function(d) { return d.date; })	// accessor for event date
			 .desc(function(d) { return d.name; })
	         .img(function(d) { return d.img; })
	        .bold(function(d) { return d.bold;})
			 .width(800);							// width of chart

		// join and render

		d3.select("#Wikiline").datum(json.events).call(chart);
	});



	//Read 

});


