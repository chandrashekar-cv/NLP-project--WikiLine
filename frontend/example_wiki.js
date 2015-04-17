d3.json("./wiki.json", function(json) {

	if (json === null) return; // parse problem, nothing to do here

	// setup data for chart
	
	json.events.forEach(function(p, i) {
		p.date = +p.date; // coerce into right type
	});

	json.events.sort(function(a,b) { return a.date < b.date ? -1 : a.date > b.date ? 1 : 0; });

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
