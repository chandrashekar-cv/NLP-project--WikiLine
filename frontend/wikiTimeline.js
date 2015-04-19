
function wikiTimelineChart() {
    var _date = function(value) { return value; };
    var _desc = function(value) { return value; };
    var _imgUrl = function(value) { return value; };
    var _boldWords = function(value) { return value; };
    
    var _entryHeight = 50; 	// spacing between each entry
	var _entryGap = 10;		// gap above the start of each entry
    var _entryOffset = 25; //  Y - offset after which cirle is placed 
    var _circleRadius = 5; // Radius of circle
    var _polygonProt = _circleRadius;
    var _entryImgWidth = 100;
    var _textHeight = 14;
	
	var _width = 0; 		// default is set later 
    
    // left & right margins of each column, including the middle line (midMargin)
	// all derived from _width - see my.width() below
	
	var _midMargin = 0;
	var _leftColMarginL = 0, _leftColMarginR = 0;
	var _rightColMarginL = 0, _rightColMarginR = 0;
    
    function my(selection) {
		selection.each(function(d, i) {
			console.log(d[i]);
			// generate chart here; 'd' is the data and 'this' is the element
            
			// establish base SVG frame
			
			var svgBase = d3.select(this).append("svg:svg")
				.attr("width", _rightColMarginR + 5)
				.attr("height", (d.length + 1.5) * _entryHeight);
            
            // draw mid-line - use number of events to determine length of the line
            
            console.log("d.length is " + d.length);
            svgBase.append("line")
				   .attr("x1", _midMargin)
				   .attr("y1", 0)
				   .attr("x2", _midMargin)
				   .attr("y2", (d.length + 1.5) * _entryHeight)
                   .attr("class", "line");
//				   .attr("stroke", "#999999")
//				   .attr("stroke-width", 5);
            
            // now bind data and draw entries

			var entryBase = svgBase.selectAll(".entry")
				                .data(d)
			                 .enter()
				                .append("g");
            
            entryBase.append("circle")
				.attr("cx", _midMargin)
				.attr("cy", function(d, i) { return i * _entryHeight + _entryGap + _entryOffset; })
				.attr("r", _circleRadius)
                .attr("class", "circle");
                            
			entryBase.append("polygon")
				.attr("points", function(d, i) {
					var yTop = i * _entryHeight + _entryGap;

					// polygon has notch on right or left depending on odd/even of index

					return (i%2 == 0) ? 
						_leftColMarginL + "," + yTop 
						+ " " + _leftColMarginR + "," + yTop 
						+ " " + _leftColMarginR + "," + (yTop + _entryOffset - _circleRadius) 
						+ " " + (_leftColMarginR+ _polygonProt) + "," + (yTop + _entryOffset) 
						+ " " + _leftColMarginR + "," + (yTop + _entryOffset + _circleRadius) 
						+ " " + _leftColMarginR + "," + (yTop + 85) 
						+ " " + _leftColMarginL + "," + (yTop + 85)
					: 
						_rightColMarginR + "," + yTop
						+ " " + _rightColMarginL + ","  + yTop
						+ " " + _rightColMarginL + ","  + (yTop + _entryOffset - _circleRadius)
						+ " " + (_rightColMarginL- _polygonProt) + "," + (yTop + _entryOffset)
						+ " " + _rightColMarginL + ","  + (yTop + _entryOffset + _circleRadius)
						+ " " + _rightColMarginL + ","  + (yTop + 85)
						+ " " + _rightColMarginR + "," + (yTop + 85);
				})
                .attr("class", "polygon");
            
            
            entryBase.append('image')
                .attr("xlink:href", function(d) { return _imgUrl(d);})
                .attr("x", function(d,i) {return (i%2 == 0) ? 
                                                    (_leftColMarginR - _entryImgWidth)
                                                    :  
                                                    (_rightColMarginR - _entryImgWidth);} )
                .attr("y", function(d,i) { return i * _entryHeight + _entryGap;})
                .attr("width", _entryImgWidth)
                .attr("height", 85);
                      
           var textBase = entryBase.append("text")
				// text is written in to left or right column, depending on odd/even of index
			
				.attr("x", function(d,i) { return ((i%2 == 0) ? _leftColMarginL : _rightColMarginL) + 4; })
				
				// set height & style of text block
				
				.attr("y", function(d, i) { return i * _entryHeight + _entryGap + 14; })
				.attr("class", "textBase");
 
			// lay out text block - date followed by event title

			textBase.append("tspan")
				.attr("class", "date")
				.text(function(d) { return _date(d); });
            
            
			textBase.append("tspan")
				.html(function(d, i) {
                        var words =  _desc(d).split(/\s+/).reverse();
                        var line = [];
                        var svgline = [];
                        var wordHtml = "";
                        var boldwords = _boldWords(d);
                        var y = i* _entryHeight + _entryGap + 2*_textHeight;
                        var x = ((i%2 == 0) ? _leftColMarginL : _rightColMarginL) + 4;
                        var wC = 0;
                        var bwC = 0;
                        while( word = words.pop()) {
                            if((boldwords != []) && boldwords[bwC] == wC) {
                                line.push("<span class=\"date\">" + word + "</span>");
                                svgline.push("<tspan class=\"date\">" + word + "</tspan>");
                                bwC += 1;
                            } else {
                                line.push(word);
                                svgline.push(word);
                            }
                            
                            $('#testSpan').html(line.join(" ")).attr("class","textBase");
                            if($("#testSpan").width() > (_leftColMarginR - _leftColMarginL -_entryImgWidth - 10)) {
                                var word = line.pop();
                                var svgword = svgline.pop();
                                wordHtml += "<tspan x=\""+ x +"\" y=\""+ y.toString() +"\">" + svgline.join(" ") + "</tspan>";
                                line = [word];
                                svgline = [svgword];
                                y += _textHeight;
                            }
                            wC += 1;
                        }
                        wordHtml += "<tspan x=\""+ x +"\" y=\""+ y.toString() +"\">" + svgline.join(" ") + "</tspan>";
                        $("#testSpan").text("");
                        return wordHtml;
                    } );			
							
				
		});
	}
    
    my.width = function(value) {
		if (!arguments.length) return _width;
		
		_width = value;
		
		_midMargin = _width/2;
		_leftColMarginR = _midMargin - 13;
		_rightColMarginL = _midMargin + 13;
		
		_leftColMarginL = 5;
		_rightColMarginR = _width - 5;
		
		return my;
	}
	
	// configuration accessors and setters
	
	my.entryHeight = function(value) {
		if (!arguments.length) return _entryHeight;
		
		_entryHeight = value;
		
		return my;
	}
	
	my.entryGap = function(value) {
		if (!arguments.length) return _entryGap;
		
		_entryGap = value;
		
		return my;
	}

	my.desc = function(value) {
		if (!arguments.length) return _desc;
		
		_desc = value;
		return my;
	}
	
	
	my.date = function(value) {
		if (!arguments.length) return _date;
		
		_date = value;
		return my;
	}
    
    my.img = function(value) {
        if(!arguments.length) return _imgUrl;
        
        _imgUrl = value;
        return my;
    }
    
    my.bold = function(value) {
        if(!arguments.length) return _boldWords;
        
        _boldWords = value;
        return my;
    }
	
	my.width(600);
	
	return my;
            
}