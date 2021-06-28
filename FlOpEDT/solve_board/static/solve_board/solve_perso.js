// This file is part of the FlOpEDT/FlOpScheduler project.
// Copyright (c) 2017
// Authors: Iulian Ober, Paul Renaud-Goud, Pablo Seban, et al.
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as
// published by the Free Software Foundation, either version 3 of the
// License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful, but
// WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
// Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public
// License along with this program. If not, see
// <http://www.gnu.org/licenses/>.
//
// You can be released from the requirements of the license by purchasing
// a commercial license. Buying such a license is mandatory as soon as
// you develop activities involving the FlOpEDT/FlOpScheduler software
// without disclosing the source code of your own applications.






/**
 *
 * The storage structure is below,
 * It is made up of different attributes that you can
 * understand thanks to the comments.Each constraint has a
 * number of parameters stored in a list.
 * constraints is a constraint list. Each constraint
 * is an object.
 *
*/

/*
let constraints = [
        {
        id: 8, // id de la TTC
        name: "Covoiturage", // nom du type de TTC
        weight: 1, // poids de la TTC
        is_active: true, // contrainte active ?
        comment: "", // commentaire sur la TTC
        last_modification: null, // date de création
        weeks : [{nb: 14 , year: 2021},{nb: 33 , year: 2021}], // week a la forme : {nb: int , year: int}
        parameters : [
            {
            name: "Prof", // nom du paramètre dans la TTC
            type: 'people.Tutor', // nom du type des objets dans ce paramètre
            required: true, // paramètre obligatoire ?
            all_except: true, // tous sauf ?
            multiple : true,
            id_list: [2,6], // ids des objets pour le paramètre dans la TTC
            acceptable: [1,2,3,4,5,6,7,8,9,10,11] // ids des objets acceptables comme valeur du paramètre
            },
            {
            name: "bonjour", // nom du paramètre dans la TTC
            type: 'people.Tutor', // nom du type des objets dans ce paramètre
            required: false, // paramètre obligatoire ?
            all_except: true, // tous sauf ?
            multiple : true,
            id_list: [1,8,5,6,7,8,9], // ids des objets pour le paramètre dans la TTC
            acceptable: [1,2,3,4,5,6,7,8,9,10,11,12] // ids des objets acceptables comme valeur du paramètre
            }]
          }];

*/


/**
 *
 * The storage structure of the parameters is below,
 * this allows you to retrieve the value associated with an id
 * found in the id_list of the parameters of a constraint.
 * It is composed of a parameters object storing another object
 * which itself stores a list. For example in the first case
 * below people and Tutor represents the type of the parameter.
 *
*/

/*
 let parameters = {
    people:{
        Tutor:[
  {
    "id": 1,
    "name": "PSE"
  },
  {
    "id": 2,
    "name": "PRG"
  }
]
   },
    base:{
        Module:[
            {"id":1,"abbrev":"AMN"},
            {"id":2,"abbrev":'AMN2'}
        ]
    }
}
*/


/**
 *
 * The structure below is a list of categories,
 * this is used to define to which category belongs
 * each constraint. A category can contain some
 * another.
 *
*/

/*
let categories = [
    {id:1,
    name: 'Tous',// nom de la catégorie
    parent:null, // catégorie parent
    constraints_list:[8,9,10], //nombre de contraintes comprises dans cette catégorie
    hidden:false},
    {id:2,
    name: 'Categorie cool',
    parent:1, // id de la categorie parent
    constraints_list:[],
    hidden:true}
]
*/




// Function allowing to retrieve all the constraints from the API
let constraints;
function fetch_constraint(){

    $.ajax({
        type:"GET",
        dataType: 'text',
        url: build_url(url_ttconstraints),
        async: false,
        contentType: "application/json",
        success: function(msg){
            constraints = JSON.parse(msg);
        },
        error: function (msg){
            console.log("error");
            show_loader(false);
        }
    })
    return constraints;
};

fetch_constraint() ;




// Function allowing to retrieve all the parameters  from the API
let parameters;
function fetch_parameters(){

    $.ajax({
        type:"GET",
        dataType: 'text',
        url: build_url(url_parameters),
        async: false,
        contentType: "application/json",
        success: function(msg){
            parameters = JSON.parse(msg);

        },
        error: function (msg){
            console.log("error");
            show_loader(false);
        }
    })
    return parameters;
};
fetch_parameters();


// Function allowing to delete all the constraints from the API
let constraints;
function fetch_constraint(){

    $.ajax({
        type:"GET",
        dataType: 'text',
        url: build_url(url_ttconstraints),
        async: false,
        contentType: "application/json",
        success: function(msg){
            constraints = JSON.parse(msg);
        },
        error: function (msg){
            console.log("error");
            show_loader(false);
        }
    })
    return constraints;
};

fetch_constraint() ;






// Variables
// The zone where we are going to create our HTML skeleton for the display of the constraints
        let consZone = document.getElementById("Zone de contrainte");
        consZone.setAttribute('id','consZone');

// Function regenerating the lines of constraints
function refresh_param() {

// Table where we will add the rows for the constraints and the columns for these attributes
        let tbl = document.createElement("table");
        tbl.setAttribute('id','table');
        let tblBody = document.createElement("tbody");
        tblBody.setAttribute('id','tableBody');


    // Loop traversing each constraint 1 by 1
     for (let l = 0; l < constraints.length; l++) {

         // Create a row
         let row = document.createElement("tr");
         row.setAttribute('class', 'ligne_contrainte');
         row.setAttribute('id', 'ligne_contrainte');


         // Selection button
         let select = document.createElement("td");
         select.setAttribute('class', 'selec_contrainte');

         // Create a checkbox button to select the constraint
         let selec = document.createElement('input');
         selec.setAttribute('type', 'checkbox');
         selec.setAttribute('id', 'selection');
         selec.setAttribute('name', 'selection');
         select.appendChild(selec);
         row.appendChild(select);


         // Name of the constraint
         let div_nom = document.createElement("td");
         div_nom.setAttribute('class', 'nom_contrainte');
         nom = document.createTextNode(constraints[l].name);
         div_nom.appendChild(nom);
         row.appendChild(div_nom);



         // Parameters of the constraint
         // tag allowing the creation of a column corresponding to the parameters
         let para = document.createElement("td");
         para.setAttribute('class', 'para_contrainte');



         // The various existing parameters of the constraint line
         for (let k = 0; k < constraints[l].parameters.length; k++) {

             if (constraints[l].parameters[k].type === "base.Department") {
                 continue;
             }

             let p_param = document.createElement("p");
             p_param.setAttribute('id', 'param' + constraints[l].parameters[k].name);
             // Parameter name in bold if it is required
             let strong = document.createElement("strong");
             // Parameter name in italics if it is not required
             let em = document.createElement("em");

             // Button used to add possibilities to a parameter
             let btn_Possib = document.createElement('input');
             btn_Possib.setAttribute('type', 'image');
             btn_Possib.setAttribute('id', 'image_Add');
             btn_Possib.setAttribute('src', '/static/base/img/ajout.png');
             btn_Possib.setAttribute('width', '15px');
             btn_Possib.setAttribute('height', '15px');


             // Button allowing the display of the possibilities zone if there are more than 2
             let btn_possibl = document.createElement('input');
             btn_possibl.setAttribute('id', 'btn_possibl');
             btn_possibl.setAttribute('type', 'button');
             btn_possibl.setAttribute('width', '15px');
             btn_possibl.setAttribute('height', '15px');
             btn_possibl.setAttribute('onclick', 'hide(\'zone_Possib' + constraints[l].parameters[k].id_list + k + '\')');
             btn_possibl.setAttribute('class', 'btn_possibl');

             // Display area of all the possibilities of a parameter
             let zone_Possib = document.createElement("div");
             zone_Possib.setAttribute('class', 'zone_Possib');
             zone_Possib.setAttribute('id', 'zone_Possib' + constraints[l].parameters[k].id_list + k);
             //type du paramètre actuel sous form de string
             let type = constraints[l].parameters[k].type;
             // Concatenate the type + parameters and remove the quotes
             let type_concat = stringGetter(type);

             for (let m = 0; m < constraints[l].parameters[k].id_list.length; m++) {
                 let tab_username = [];
                 type_concat.find(function (n) {
                     if (n.id === constraints[l].parameters[k].id_list[m]) {
                         let list_values = Object.values(n);
                         tab_username.push(list_values[1]);
                     }
                 });
                 for (let h = 0; h < tab_username.length; h++) {
                     let possib = document.createTextNode(tab_username[h] + " ");
                     // if there is only one value in the id_list
                     if (constraints[l].parameters[k].id_list.length === 1) {
                         btn_possibl.value = tab_username[h];
                         btn_possibl.disabled = true;
                     } else {
                         type_concat.find(function (n) {
                             // if there is more than 1 values in the id_list
                             if (n.id === constraints[l].parameters[k].id_list[0]) {
                                 let list_values = Object.values(n);
                                 btn_possibl.value = list_values[1] + "...";
                             }
                         });
                         zone_Possib.appendChild(possib);

                     }
                 }
             }

             // Button for deleting a parameter
             let btn_Suppr = document.createElement('input');
             btn_Suppr.setAttribute('type', 'image');
             btn_Suppr.setAttribute('id', 'image_Delete');
             btn_Suppr.setAttribute('src', '/static/base/img/suppression.png');
             btn_Suppr.addEventListener('click', () => suppr(constraints[l].parameters[k].id_list));
             btn_Suppr.setAttribute('width', '15px');
             btn_Suppr.setAttribute('height', '15px');


             // If there are no possibilities found in parameters, then we display none
             let btn_None = document.createElement('input');
             btn_None.setAttribute('id', 'None');
             btn_None.setAttribute('type', 'button');
             btn_None.setAttribute('value', 'None');
             btn_None.setAttribute('width', '15px');
             btn_None.setAttribute('height', '15px');



             // The name of the current parameter
             let parametres_nom = document.createTextNode("  " + constraints[l].parameters[k].name + "  ");

             // Condition used to check if a parameter is required and if it is not empty
             if (constraints[l].parameters[k].required === true && constraints[l].parameters[k].id_list.length !== 0) {
                 let case_param_required = document.createElement("div");
                 case_param_required.setAttribute('class', 'case_param_required');
                 strong.appendChild(parametres_nom);
                 p_param.appendChild(strong);
                 case_param_required.appendChild(p_param);
                 case_param_required.appendChild(btn_Possib);

                 // Condition if the btn is empty then display none otherwise display the button correctly
                 if (btn_possibl.value === "") {
                     case_param_required.appendChild(btn_None);
                     btn_None.disabled = true;
                 } else {
                     case_param_required.appendChild(btn_possibl);
                 }
                 case_param_required.appendChild(btn_Suppr);
                 case_param_required.appendChild(zone_Possib);
                 para.appendChild(case_param_required);

             // Condition used to display the non-required parameters
             } else if (constraints[l].parameters[k].id_list.length !== 0) {
                 let case_param_second = document.createElement("div");
                 case_param_second.setAttribute('class', 'case_param_second');
                 em.appendChild(parametres_nom);
                 p_param.appendChild(em);
                 case_param_second.appendChild(p_param);
                 case_param_second.appendChild(btn_Possib);

                // Condition if the btn is empty then display none otherwise display the button correctly
                 if (btn_possibl.value === "") {
                     case_param_second.appendChild(btn_None);
                     btn_None.disabled = true;
                 } else {
                     case_param_second.appendChild(btn_possibl);
                 }
                 case_param_second.appendChild(btn_Suppr);
                 case_param_second.appendChild(zone_Possib);
                 para.appendChild(case_param_second);
             }

         }

         row.appendChild(para);


         // Adding a column for button insertion
         let ajout_Param = document.createElement("td");
         ajout_Param.setAttribute('class', 'ajout_param');

        // Button used to display the drop-down menu
         let btn = document.createElement('input');
         btn.setAttribute('type', 'image');
         btn.setAttribute('id', 'image_Add');
         btn.setAttribute('src', '/static/base/img/ajout.png');
         btn.setAttribute('width', '20px');
         btn.setAttribute('height', '20px');
         btn.setAttribute('onclick', 'hide(\'Menu' + l + '\')');
         ajout_Param.appendChild(btn);

         // Validate the selected parameters to add
         let btn_valid_param = document.createElement('input');
         btn_valid_param.setAttribute('type', 'button');
         btn_valid_param.setAttribute('id', 'valider' + l);
         btn_valid_param.setAttribute('value', 'Valider');
         btn_valid_param.setAttribute('width', '20px');
         btn_valid_param.setAttribute('height', '20px');
         row.appendChild(ajout_Param);


         // Add the zone allowing the display of the drop-down menu
         let Menu = document.createElement("div");
         Menu.setAttribute('id', 'Menu' + l);
         Menu.setAttribute('class', 'Menu');
         let Select = document.createElement("select");
         Select.setAttribute('id', 'ChoixP' + l);
         Select.setAttribute('data-max', '');
         Select.setAttribute('multiple', 'multiple');
         Select.setAttribute('style', '');
         Menu.appendChild(Select);
         Menu.appendChild(btn_valid_param);
         ajout_Param.appendChild(Menu);
         row.appendChild(ajout_Param);

         // Activate a row
         let activ = document.createElement("td");
         activ.setAttribute('class', 'activ_contrainte');
         let activate = document.createElement('input');
         activate.setAttribute('type', 'checkbox');
         activate.setAttribute('id', 'activation');
         activate.setAttribute('name', 'activation');
         activate.setAttribute('onclick', 'activate(this,constraints[' + l + '])');
         activ.appendChild(activate);
         row.appendChild(activ);


        // If a constraint is active, then the button will be checked
         if (constraints[l].is_active === true) {
             activate.checked = true;
         }


        // Select the weight of a constraint
         let range_td = document.createElement("td");
         range_td.setAttribute('class', 'poid_contrainte');


         // Button used to manage the weight of a constraint
         let slide_btn = document.createElement('input');
         slide_btn.setAttribute('type', 'range');
         slide_btn.setAttribute('min', '1');
         slide_btn.setAttribute('max', '8');
         slide_btn.setAttribute('value', constraints[l].weight);
         slide_btn.setAttribute('onclick', 'update_weight(this,constraints[' + l + '])');
         slide_btn.setAttribute('class', 'range-slider__range');
         slide_btn.setAttribute('id', 'Weight');
         slide_btn.setAttribute('name', 'Weight');
         range_td.appendChild(slide_btn);
         row.appendChild(range_td);

         // Duplicate a constraint line
         let duplic = document.createElement("td");
         duplic.setAttribute('class', 'duplic_contrainte');
         let btn_duplicate = document.createElement('input');
         btn_duplicate.setAttribute('type', 'image');
         btn_duplicate.setAttribute('id', 'image_duplic');
         btn_duplicate.setAttribute('src', '/static/base/img/copier-coller-1.png');
         btn_duplicate.setAttribute('width', '25px');
         btn_duplicate.setAttribute('height', '25px');
         // Validating a row and sending to the API
         let btn_Validate = document.createElement('input');
         btn_Validate.setAttribute('type', 'image');
         btn_Validate.setAttribute('id', 'image_Validate');
         btn_Validate.setAttribute('src', '/static/base/img/valider.png');
         btn_Validate.setAttribute('onclick', 'update_send(constraints,parameters)');
         btn_Validate.setAttribute('width', '25px');
         btn_Validate.setAttribute('height', '25px');
         duplic.appendChild(btn_duplicate);
         duplic.appendChild(btn_Validate);
         //Deleting a constraint
         let btn_delete = document.createElement('input');
         btn_delete.setAttribute('type', 'image');
         btn_delete.setAttribute('id', 'image_Validate');
         btn_delete.setAttribute('src', '/static/base/img/LasuppressiondesIRP.png');
         btn_delete.setAttribute('onclick', 'suppr_contstraint('+l+','+constraints[l].name+')');
         btn_delete.setAttribute('width', '25px');
         btn_delete.setAttribute('height', '25px');
         duplic.appendChild(btn_delete);
         row.appendChild(duplic);

         // Adding the row to the table
         tblBody.appendChild(row);
     }
// Adding the generate table in the HTML area
    tbl.appendChild(tblBody);
     consZone.appendChild(tbl);
 }
refresh_param();
create_menu();

//Function transforming a string into a path that can be used to browse a list and / or a JS object
function stringGetter (getter) {
        return getter
        .split('.')
        .reduce((o,i)=>o[i], parameters);
      }


/**
 * Deleting a Parameter
 * @param param
 *
 */
function suppr(param){
    param.length=0;
    document.getElementById('tableBody').remove();
    // Regeneration of the constraint lines
    refresh_param();
    // Create new drop-down menus
    create_menu();
}

/**
 * Deleting a Constraints
 * @param param
 *
 */
function suppr_contstraint(index,constraint_name){



    if (confirm("Êtes-vous sûr de vouloir supprimer cette contrainte ?")) {
        // Delete the constraints
        if (index !== -1) constraints.splice(index, 1);
        alert("La contrainte à été supprimée avec succés.");
    } else {
        // Do nothing!
        alert("La contrainte n'a pas été supprimée.");
    }

    document.getElementById('tableBody').remove();
    // Regeneration of the constraint lines
    refresh_param();
    // Create new drop-down menus
    create_menu();
}

/**
 * Activation / deactivation of a parameter
 * @param param
 *
 */
function activate(checkbox,param){
      if (checkbox.checked) {
                param.is_active = true;
            }
            else {
                param.is_active = false;
            }

}

/**
 * Managing the weight of a constraint
 * @param slider, param
 *
 *
 */
function update_weight(slider,param){
    param.weight = slider.value;
}

/**
 * Sending the modified constraint to the API
 * @param constr,param
 *
 *
 */
function update_send(constr,param){
   console.log(constr);
   console.log(param);
}


/**
 * Show/hide an élement
 *
 */
     function hide(id) {
        let x = document.getElementById(id);
        if (x.style.display === "block") {
            x.style.display = "none";
        } else {
            x.style.display = "block";
        }
    }


// Function allowing the generation of the drop-down menu of options
function create_menu() {
    for (let cpt = 0; cpt < constraints.length; cpt++) {
        var ldd = document.getElementById("ChoixP" + cpt);

        //Creation of the option menu that is filled.
        for (let j = 0; j < constraints[cpt].parameters.length; j++) {
            if (constraints[cpt].parameters[j].id_list.length == 0) {
                var opt = document.createElement('option');
                opt.innerHTML = constraints[cpt].parameters[j].name;
                ldd.appendChild(opt);
            }
        }

        // javascript from the drop-down menu allowing selection
        $("#ChoixP" + cpt).easySelect({
            buttons: true,
            search: true,
            placeholder: 'Choisissez un paramètre',
            placeholderColor: 'violet',
            selectColor: 'lila',
            itemTitle: 'Color selected',
            showEachItem: true,
            width: '100%',
            dropdownMaxHeight: '450px',
        })


// Listener allowing to return the selected elements in the easyselect
        $('#valider' + cpt).click(function () {
            $('#ChoixP' + cpt + ' option:selected').each(function () {
                str = $(this).text() + " ";
                val = $(this).val();
            })
        });

    }
}





