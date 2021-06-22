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


let constraints;

function myCallback(result) {
    // Code that depends on 'result'
}






function fetch_constraint(){

    $.ajax({
        type:"GET",
        dataType: 'text',
        url: build_url(url_ttconstraints),
        async: true,
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


fetch_constraint();


let parameters = {
    "people":{
        Tutor:[
  {
    "id": 1,
    "name": "PSE"
  },
  {
    "id": 2,
    "name": "PRG"
  },
  {
    "id": 3,
    "name": "AV"
  },
  {
    "id": 4,
    "name": "BBCB"
  },
  {
    "id": 5,
    "name": "BC"
  },
  {
    "id": 6,
    "name": "BCPV"
  },
  {
    "id": 7,
    "name": "BDB"
  },
  {
    "id": 8,
    "name": "BEFT"
  },
  {
    "id": 9,
    "name": "BFLT"
  },
  {
    "id": 10,
    "name": "BK"
  },
  {
    "id": 11,
    "name": "BM"
  },
  {
    "id": 12,
    "name": "BMB"
  },
  {
    "id": 13,
    "name": "BMBJ"
  }
]
    },
    base:{
        Module:[
            {"id":1,"abbrev":"AMN"},
            {"id":2,"abbrev":'AMN2'},
            {"id":3,"abbrev":'AMN3'},
            {"id":4,"abbrev":'AMN4'}
        ]
    }
}

let categories = [
    {id:1,
    name: 'Tous',
    parent:null,
    constraints_list:[8,9,10],
    hidden:false},
    {id:2,
    name: 'Categorie cool',
    parent:1,
    constraints_list:[],
    hidden:true}
]







//Variables
let consZone = document.getElementById("Zone de contrainte");
let tbl = document.createElement("table");
let tblBody = document.createElement("tbody");
let parametres;
let str;
let val;
//Boucle parcourant chaque contrainte 1 par 1
let nom;

let case_param_required = document.getElementsByTagName("body")[0];

for (let l = 0; l < constraints.length; l++) {

    // creation d'une colonne
    let row = document.createElement("tr");
    row.setAttribute('class', 'ligne_contrainte')

    // Bouton sélection

    let select = document.createElement("td");
    select.setAttribute('class', 'selec_contrainte')
    let selec = document.createElement('input');
    selec.setAttribute('type', 'checkbox');
    selec.setAttribute('id', 'selection');
    selec.setAttribute('name', 'selection');
    select.appendChild(selec);
    row.appendChild(select);



    //Nom de la contrainte
    let div_nom = document.createElement("td");
    div_nom.setAttribute('class', 'nom_contrainte');
    nom = document.createTextNode(constraints[l].name);
    div_nom.appendChild(nom);
    row.appendChild(div_nom);

// Parametres de la contraintes
    let para = document.createElement("td");
    para.setAttribute('class', 'para_contrainte');


    //Les différents parametres existants de la ligne de contrainte
    for (let k = 0; k < constraints[l].parameters.length; k++) {
        let p_param = document.createElement("p");
        p_param.setAttribute('id','param'+constraints[l].parameters[k].name);
        let strong = document.createElement("strong");
        let em = document.createElement("em");


        let btn_Possib = document.createElement('input');
        btn_Possib.setAttribute('type', 'image');
        btn_Possib.setAttribute('id', 'image_Add');
        btn_Possib.setAttribute('src', '/static/base/img/ajout.png');
        btn_Possib.setAttribute('width', '15px');
        btn_Possib.setAttribute('height', '15px');

        //Zone d'affichage des attributs d'un paramètre
        let btn_possibl = document.createElement('input');
        btn_possibl.setAttribute('id', 'btn_possibl');
        btn_possibl.setAttribute('type', 'button');
        btn_possibl.setAttribute('width', '15px');
        btn_possibl.setAttribute('height', '15px');
        btn_possibl.setAttribute('onclick', 'hide(\'zone_Possib'+k+'\')');
        btn_possibl.setAttribute('class', 'btn_possibl');

        let zone_Possib = document.createElement("div");
        zone_Possib.setAttribute('class', 'zone_Possib' );
        zone_Possib.setAttribute('id', 'zone_Possib'+k );

        let type = constraints[l].parameters[k].type;
        let type_concat = stringGetter(type);


            for(let m = 0; m < constraints[l].parameters[k].id_list.length; m++ ) {
                let tab_username = [];

                type_concat.find(function(n){

                   if(n.id === constraints[l].parameters[k].id_list[m]){
                       let id = n.id-1;
                     let list_key = Object.keys(n);
                     let second_key = list_key[1];
                     let zi_key = type+"."+id+"."+second_key;
                     let third_key = stringGetter(zi_key);

                     tab_username.push(third_key);
                   }
                });
                for(let h = 0;h<tab_username.length;h++) {
                  let possib = document.createTextNode(tab_username[h] + " ");
                  if( constraints[l].parameters[k].id_list.length===1) {
                      btn_possibl.value = tab_username[h];
                      btn_possibl.disabled=true;

                  }else{
                    type_concat.find(function(n){
                      if(n.id === constraints[l].parameters[k].id_list[0]){
                          let id = n.id-1;
                        let list_key_1 = Object.keys(n);
                        let second_key_1 = list_key_1[1];
                        let zi_key_1 = type+"."+id+"."+second_key_1;
                        let third_key_1 = stringGetter(zi_key_1);
                        btn_possibl.value= third_key_1+"...";
                      }
                    });
                    zone_Possib.appendChild(possib);

                  }
                }
            }




        let btn_Suppr = document.createElement('input');
        btn_Suppr.setAttribute('type', 'image');
        btn_Suppr.setAttribute('id', 'image_Delete');
        btn_Suppr.setAttribute('src', '/static/base/img/suppression.png');
        btn_Suppr.addEventListener('click', () => suppr(constraints[l].parameters[k].id_list));
        btn_Suppr.setAttribute('width', '15px');
        btn_Suppr.setAttribute('height', '15px');

        let btn_None = document.createElement('input');
        btn_None.setAttribute('id', 'None');
        btn_None.setAttribute('type', 'button');
        btn_None.setAttribute('value', 'None');
        btn_None.setAttribute('width', '15px');
        btn_None.setAttribute('height', '15px');



        if (constraints[l].parameters[k].id_list.length != 0) {

            parametres = document.createTextNode("  " + constraints[l].parameters[k].name + "  ");
            if (constraints[l].parameters[k].required === true) {
                let case_param_required = document.createElement("div");
                case_param_required.setAttribute('class', 'case_param_required');
                strong.appendChild(parametres);
                p_param.appendChild(strong);
                case_param_required.appendChild(p_param);
                case_param_required.appendChild(btn_Possib);
                if(btn_possibl.value === ""){
                case_param_required.appendChild(btn_None);
                btn_None.disabled = true;
                }else {
                    case_param_required.appendChild(btn_possibl);
                }
                case_param_required.appendChild(btn_Suppr);
                case_param_required.appendChild(zone_Possib);
                 para.appendChild(case_param_required);

            } else {
                let case_param_second = document.createElement("div");
                case_param_second.setAttribute('class', 'case_param_second');
                em.appendChild(parametres);
                p_param.appendChild(em);
                case_param_second.appendChild(p_param);
                case_param_second.appendChild(btn_Possib);
                if(btn_possibl.value === ""){
                case_param_second.appendChild(btn_None);
                btn_None.disabled = true;
                }else {
                    case_param_second.appendChild(btn_possibl);
                }
                case_param_second.appendChild(btn_Suppr);
                case_param_second.appendChild(zone_Possib);
                para.appendChild(case_param_second);

            }

        }

    }
    row.appendChild(para);

    //Bouton permettant l'affichage du menu déroulant
    let ajout_Param = document.createElement("td");
    ajout_Param.setAttribute('class', 'ajout_param');
    let btn = document.createElement('input');
    btn.setAttribute('type', 'image');
    btn.setAttribute('id', 'image_Add');
    btn.setAttribute('src', '/static/base/img/ajout.png');
    btn.setAttribute('width', '20px');
    btn.setAttribute('height', '20px');
    btn.setAttribute('onclick', 'hide(\'Menu'+l+'\')');
    ajout_Param.appendChild(btn);
    let btn_valid_param = document.createElement('input');
    btn_valid_param.setAttribute('type', 'button');
    btn_valid_param.setAttribute('id', 'valider'+l);
    btn_valid_param.setAttribute('value', 'Valider');
    btn_valid_param.setAttribute('width', '20px');
    btn_valid_param.setAttribute('height', '20px');
    row.appendChild(ajout_Param);


    //Ajout de la zone permettant l'affichage du menu déroulant
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

    //Activation d'une ligne
    let activ = document.createElement("td");
    activ.setAttribute('class', 'activ_contrainte');
    let activate = document.createElement('input');
    activate.setAttribute('type', 'checkbox');
    activate.setAttribute('id', 'activation');
    activate.setAttribute('name', 'activation');
    activ.appendChild(activate);
    row.appendChild(activ);

    if (constraints[l].is_active === true) {
        activate.checked = true;
    }

    // Selection du poids
    let range_td = document.createElement("td");
    range_td.setAttribute('class', 'poid_contrainte');


    let slide_btn = document.createElement('input');
    slide_btn.setAttribute('type', 'range');
    slide_btn.setAttribute('min', '1');
    slide_btn.setAttribute('max', '8');
    slide_btn.setAttribute('value', constraints[l].weight);
    slide_btn.setAttribute('class', 'range-slider__range');
    slide_btn.setAttribute('id', 'Weight');
    slide_btn.setAttribute('name', 'Weight');
    range_td.appendChild(slide_btn);
    row.appendChild(range_td);

    // Duplication
    let duplic = document.createElement("td");
    duplic.setAttribute('class', 'duplic_contrainte');
    let btn_duplicate = document.createElement('input');
    btn_duplicate.setAttribute('type', 'image');
    btn_duplicate.setAttribute('id', 'image_duplic');
    btn_duplicate.setAttribute('src', '/static/base/img/copier-coller-1.png');
    btn_duplicate.setAttribute('width', '25px');
    btn_duplicate.setAttribute('height', '25px');
    let btn_Validate = document.createElement('input');
    btn_Validate.setAttribute('type', 'image');
    btn_Validate.setAttribute('id', 'image_Validate');
    btn_Validate.setAttribute('src', '/static/base/img/valider.png');
    btn_Validate.setAttribute('width', '25px');
    btn_Validate.setAttribute('height', '25px');
    duplic.appendChild(btn_duplicate);
    duplic.appendChild(btn_Validate);
    row.appendChild(duplic);

    // add the row to the end of the table body
    tblBody.appendChild(row);

}

//function index(obj,i) {return obj[i]}

tbl.appendChild(tblBody);
consZone.appendChild(tbl);

//Fonction transformant un string en un objet
function stringGetter (getter) {
        return getter
        .split('.')
        .reduce((o,i)=>o[i], parameters);
      }

      // Tentative de sauvegarde du fichier js modifié
      /*function suppr(param){
            var old_data = param;
            var new_data = [];
            console.log(localStorage.setItem(param,'[]'));
            localStorage.removeItem(param);

    }*/

 //Fonction permettant la suppression d'un parametre ( pour l'instant seulement dans la console)
function suppr(param){
    console.log(param);
    param.length=0;
    console.log(param);
}


//Fonction permettant de cacher un élément
     function hide(id) {
        let x = document.getElementById(id);
        if (x.style.display === "block") {
            x.style.display = "none";
        } else {
            x.style.display = "block";
        }
    }

// Boucle permettant la génération du menu déroulant des options
for(let cpt=0;cpt<constraints.length;cpt++){

    var ldd = document.getElementById("ChoixP"+cpt);

      for(let j =0;j<constraints[cpt].parameters.length;j++){
            if(constraints[cpt].parameters[j].id_list.length==0 ) {
                var opt = document.createElement('option');
                opt.innerHTML = constraints[cpt].parameters[j].name;
                ldd.appendChild(opt);
            }
        }



    $("#ChoixP"+cpt).easySelect({
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


// Listener permettant de retourner les elements selectionner dans le easyselect
$('#valider'+cpt).click( function(){
          $('#ChoixP'+cpt+' option:selected').each(function(){
             str = $(this).text() + " ";
             val = $(this).val();
            console.log(str,val);
        })
        });

}






