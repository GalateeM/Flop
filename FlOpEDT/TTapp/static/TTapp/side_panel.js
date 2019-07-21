// open side panel
function openNav() {

    is_side_panel_open = true ;

    // open panel
    document.getElementById("side_panel").style.width = "250px";
    document.getElementById("edt-main").style.marginLeft = "250px";
    document.getElementById("menu-edt").style.marginLeft = "250px";

    // add event listener
    $('#dd_work_copy').on('change', function (e) {
        num_copie = this.value;
        fetch_all(false, false);
    });

    // fetch the copy numbers
    fetch_work_copy_numbers();
}

// Fetch the available work copy numbers for the current week
function fetch_work_copy_numbers() {
    var cur_week = weeks.init_data[weeks.sel[0]].semaine;
    var cur_year = weeks.init_data[weeks.sel[0]].an;

    $.ajax({
        type: "GET",
        dataType: 'json',
        url: url_work_copies +  cur_year + '/' + cur_week,
        async: true,
        contentType: "application/json; charset=utf-8",
        success: function(msg) {
            update_work_copy_numbers(msg.copies) ;
        },
        error: function(msg) {
            console.log("error");
        }
    });

}

// refresh the work copy dropdown list
function update_work_copy_numbers(copies) {
    // remove old copy numbers
    var dd = document.getElementById("dd_work_copy");
    while (dd.firstChild) {
        dd.removeChild(dd.firstChild);
    }
    
    // add new copy numbers
    var option ;
    for (var i=0 ; i<copies.length ; i++){
        option = {value:copies[i], text:copies[i]} ;
        $('#dd_work_copy').append($('<option>', option));
    }
}

// close the side panel
function closeNav() {
    // avoid fetching work copy numbers if closed
    is_side_panel_open = false ;

    // close panel
    document.getElementById("side_panel").style.width = "0";
    document.getElementById("edt-main").style.marginLeft= "0";
    document.getElementById("menu-edt").style.marginLeft= "0";

}


// swap the current work copy with the public work copy, i.e. #0
// display the old public copy afterwards
function swap_with_copy_0() {
    var cur_week = weeks.init_data[weeks.sel[0]].semaine;
    var cur_year = weeks.init_data[weeks.sel[0]].an;

    show_loader(true);
    $.ajax({
        type: "GET",
        dataType: 'json',
        url: url_swap +  cur_year + '/' + cur_week + '/' + num_copie,
        async: true,
        contentType: "application/json; charset=utf-8",
        success: function(msg) {
            fetch_all(false, false);
            show_loader(false);
        },
        error: function(msg) {
            console.log("error");
            show_loader(false);
        }
    });
}


// reassign rooms and reload
function reassign_rooms() {
    var cur_week = weeks.init_data[weeks.sel[0]].semaine;
    var cur_year = weeks.init_data[weeks.sel[0]].an;

    show_loader(true);
    $.ajax({
        type: "GET",
        dataType: 'json',
        url: url_reassign_rooms +  cur_year + '/' + cur_week + '/' + num_copie,
        async: true,
        contentType: "application/json; charset=utf-8",
        success: function(msg) {
            fetch_all(false, false);
            show_loader(false);
        },
        error: function(msg) {
            console.log("error");
            show_loader(false);
        }
    });
}
