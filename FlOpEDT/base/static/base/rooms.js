/*------------------------
  ---- READ DATA FILE ----
  ------------------------*/


function fetch_rooms() {

    $.ajax({
        type: "GET",
        dataType: 'text',
        url: url_data_rooms,
        async: true,
        contentType: "text/csv",
        success: function(msg, ts, req) {
            buildings = ['A','B','C'];
            floors=[0,1,2]
            rooms = d3.csvParse(msg, translate_rooms_from_csv);

            display_rooms() ;
            display_rooms_grid() ;
        },
        error: function(msg) {
            console.log("error");
        }
    });

}


function translate_rooms_from_csv(d) {
    var ro = {
        building: d.building,
        floor: d.floor,
        name: d.name,
		has_problem: d.has_problem,
    };
    return ro;
}

function display_rooms_grid() {
    var c_layer = d3.select(".rooms-grid-layer");

    var c_all = c_layer
        .selectAll(".floor")
        .data(floors) ;

    c_all
        .enter()
        .append("g")
        .attr("class", "floor") ;
}

function display_rooms() {
    var r_layer = d3.select(".rooms-layer");

    var r_all = r_layer
        .selectAll(".room")
        .data(rooms) ;

    var r_groups = r_all
        .enter()
        .append("g")
        .attr("class", "room") ;

    r_groups
        .append("rect")
        .attr("x", room_x)
        .attr("y", room_y)
        .attr("width", room_width)
        .attr("height", room_height);

    r_groups
        .append("text")
        .text(room_txt)
        .attr("x",room_mid_x)
        .attr("y",room_mid_y);

}


/*---------------------
  -- DISPLAY HELPERS --
  ---------------------*/
function room_x(c) {
    return 200  ;
}
function room_width(c) {
    return 300 ;
}
function room_y(c) {
    return c.floor*200  ;
}
function room_mid_y(c) {
    return c.floor*200 + 150  ;
}
function room_mid_x(c) {
    return 350  ;
}
function room_height(c) {
    return 300 ;
}
function course_fill(c) {
    return 'black' ;
}

function course_txt_fill(c) {
    return 'black' ;
}

function room_txt(c) {
    return c.name ;
}

function svg_height() {
    return (day_end - day_start) * min_to_px + 200 ;
}
function svg_width() {
    return days.length * gp.nb_max * gp.width;
}
/*---------------------
        -- RUN --
  ---------------------*/

fetch_rooms();