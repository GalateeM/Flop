
var nb_columns =  15; //import nb from nb rooms
var nb_lines = 8;

var width = 1500; 
var height = 800;

var len_square = 0;

if (height/nb_lines >= width/nb_columns){
	len_square = width/nb_columns;
}else{
	len_square = height/nb_lines;
}


for (var j = 0; j < nb_lines ; j++){
	for (var i = 0; i< nb_columns; i++) {
		d3.select("svg#grille")
			.append("rect")
			.attr("width", len_square )
			.attr("height", len_square)
			.attr("x", len_square * i)
			.attr("y", len_square * j)
			.attr("stroke", "black")
			.attr("fill", "#B0F2B6");
	}
}

