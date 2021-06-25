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
 * La structure de stockage des contraintes est ci-dessous,
 * Elle est composé de différents attributs que vous pouvez
 * comprendre grâce aux commentaires.Chaque contrainte à un
 * certain nombre de paramètres stockés dans une liste.
 * constraints est une liste de contrainte. Chaque contrainte
 * est un objet.
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
 * La structure de stockage des parameters est ci-dessous,
 * celle-ci permet de récuperer la valeur associé à un id
 * se trouvant dans l'id_list des paramètres d'une contrainte.
 * Elle est composé d'un objet parameters stockant un autre objet
 * qui lui même stocke une liste. Par exemple dans le premier cas
 * ci-dessous people et Tutor représente le type du paramètre.
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
 * La structure ci-dessous est une liste de categories,
 * celle-ci sert à définir à quel catégorie appartient
 * chaque contrainte. Une catégorie peut en contenir
 * une autre.
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



// Fonction permettant de récuperer toute les contraintes de la BD à partir de l'API
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


// Fonction permettant de récuperer tout les parameters de la BD à partir de l'API
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









//Variables
// La zone où l'on va venir créer notre squelette HTML pour l'affichage des contraintes
     let consZone = document.getElementById("Zone de contrainte");
        consZone.setAttribute('id','consZone');
        function refresh_param() {
// Table où l'on va ajouter les lignes pour les contraintes et les colonnes pour ces attributs
     let tbl = document.createElement("table");
        tbl.setAttribute('id','table');

     let tblBody = document.createElement("tbody");
        tblBody.setAttribute('id','tableBody');


//Boucle parcourant chaque contrainte 1 par 1
     for (let l = 0; l < constraints.length; l++) {

         // creation d'une ligne
         let row = document.createElement("tr");
         row.setAttribute('class', 'ligne_contrainte');
         row.setAttribute('id', 'ligne_contrainte');


         // Bouton sélection
         let select = document.createElement("td");
         select.setAttribute('class', 'selec_contrainte');
         // Création d'un bouton checkbox pour sélectionner la contrainte
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


         //Parametres de la contraintes
         // balise permettant la création d'une colonne correspondant aux paramètres
         let para = document.createElement("td");
         para.setAttribute('class', 'para_contrainte');


         //Les différents parametres existants de la ligne de contrainte
         for (let k = 0; k < constraints[l].parameters.length; k++) {

             if (constraints[l].parameters[k].type === "base.Department") {
                 continue;
             }

             let p_param = document.createElement("p");
             p_param.setAttribute('id', 'param' + constraints[l].parameters[k].name);
             // Nom du paramètre en gras s'il est obligatoire
             let strong = document.createElement("strong");
             // Nom du paramètre en italique s'il n'est pas obligatoire
             let em = document.createElement("em");

             //Bouton permettant l'ajout de possibilités à un paramètre
             let btn_Possib = document.createElement('input');
             btn_Possib.setAttribute('type', 'image');
             btn_Possib.setAttribute('id', 'image_Add');
             btn_Possib.setAttribute('src', '/static/base/img/ajout.png');
             btn_Possib.setAttribute('width', '15px');
             btn_Possib.setAttribute('height', '15px');


             //Bouton permettant l'affichage de la zone des possibilités s'il y en a plus que 2
             let btn_possibl = document.createElement('input');
             btn_possibl.setAttribute('id', 'btn_possibl');
             btn_possibl.setAttribute('type', 'button');
             btn_possibl.setAttribute('width', '15px');
             btn_possibl.setAttribute('height', '15px');
             btn_possibl.setAttribute('onclick', 'hide(\'zone_Possib' + constraints[l].parameters[k].id_list + k + '\')');
             btn_possibl.setAttribute('class', 'btn_possibl');
             // Zone d'affichage de toutes les possibilités d'un paramètre
             let zone_Possib = document.createElement("div");
             zone_Possib.setAttribute('class', 'zone_Possib');
             zone_Possib.setAttribute('id', 'zone_Possib' + constraints[l].parameters[k].id_list + k);
             //type du paramètre actuel sous form de string
             let type = constraints[l].parameters[k].type;
             //Concaténation du type + parameters et suppression des guillemets
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
                     // s'il y a qu'un seule valeur dans l'id_list
                     if (constraints[l].parameters[k].id_list.length === 1) {
                         btn_possibl.value = tab_username[h];
                         btn_possibl.disabled = true;
                     } else {
                         type_concat.find(function (n) {
                             //s'il y a plus d'1 valeurs dans l'id_list
                             if (n.id === constraints[l].parameters[k].id_list[0]) {
                                 let list_values = Object.values(n);
                                 btn_possibl.value = list_values[1] + "...";
                             }
                         });
                         zone_Possib.appendChild(possib);

                     }
                 }
             }

             //Bouton de suppression d'un paramètre
             let btn_Suppr = document.createElement('input');
             btn_Suppr.setAttribute('type', 'image');
             btn_Suppr.setAttribute('id', 'image_Delete');
             btn_Suppr.setAttribute('src', '/static/base/img/suppression.png');
             btn_Suppr.addEventListener('click', () => suppr(constraints[l].parameters[k].id_list));
             btn_Suppr.setAttribute('width', '15px');
             btn_Suppr.setAttribute('height', '15px');

             //S'il n'y a pas de possibilités trouvable dans parameters, alors on affiche none
             let btn_None = document.createElement('input');
             btn_None.setAttribute('id', 'None');
             btn_None.setAttribute('type', 'button');
             btn_None.setAttribute('value', 'None');
             btn_None.setAttribute('width', '15px');
             btn_None.setAttribute('height', '15px');


             //Le nom du paramètre actuel
             let parametres_nom = document.createTextNode("  " + constraints[l].parameters[k].name + "  ");
             //Condition permettant de verifier si un paramètre est obligatoire et s'il n'est pas vide
             if (constraints[l].parameters[k].required === true && constraints[l].parameters[k].id_list.length !== 0) {
                 let case_param_required = document.createElement("div");
                 case_param_required.setAttribute('class', 'case_param_required');
                 strong.appendChild(parametres_nom);
                 p_param.appendChild(strong);
                 case_param_required.appendChild(p_param);
                 case_param_required.appendChild(btn_Possib);
                 // Condition si le btn est vide alors afficher none sinon afficher le bouton correctement
                 if (btn_possibl.value === "") {
                     case_param_required.appendChild(btn_None);
                     btn_None.disabled = true;
                 } else {
                     case_param_required.appendChild(btn_possibl);
                 }
                 case_param_required.appendChild(btn_Suppr);
                 case_param_required.appendChild(zone_Possib);
                 para.appendChild(case_param_required);
                 //Condition permettant d'afficher les paramètre non obligatoire
             } else if (constraints[l].parameters[k].id_list.length !== 0) {
                 let case_param_second = document.createElement("div");
                 case_param_second.setAttribute('class', 'case_param_second');
                 em.appendChild(parametres_nom);
                 p_param.appendChild(em);
                 case_param_second.appendChild(p_param);
                 case_param_second.appendChild(btn_Possib);
                 // Condition si le btn est vide alors afficher none sinon afficher le bouton correctement
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


         //Colonne d'ajout du bouton
         let ajout_Param = document.createElement("td");
         ajout_Param.setAttribute('class', 'ajout_param');
         //Bouton permettant l'affichage du menu déroulant
         let btn = document.createElement('input');
         btn.setAttribute('type', 'image');
         btn.setAttribute('id', 'image_Add');
         btn.setAttribute('src', '/static/base/img/ajout.png');
         btn.setAttribute('width', '20px');
         btn.setAttribute('height', '20px');
         btn.setAttribute('onclick', 'hide(\'Menu' + l + '\')');
         ajout_Param.appendChild(btn);
         //Validation des paramètres selectionnés à ajouter
         let btn_valid_param = document.createElement('input');
         btn_valid_param.setAttribute('type', 'button');
         btn_valid_param.setAttribute('id', 'valider' + l);
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
         activate.setAttribute('onclick', 'activate(this,constraints[' + l + '])');
         activ.appendChild(activate);
         row.appendChild(activ);

         // Si une contrainte est active, alors le bouton sera coché
         if (constraints[l].is_active === true) {
             activate.checked = true;
         }

         // Selection du poids d'une contrainte
         let range_td = document.createElement("td");
         range_td.setAttribute('class', 'poid_contrainte');


         // Bouton permettant la gestion du poids d'une contrainte
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

         // Duplication d'une ligne de contrainte
         let duplic = document.createElement("td");
         duplic.setAttribute('class', 'duplic_contrainte');
         let btn_duplicate = document.createElement('input');
         btn_duplicate.setAttribute('type', 'image');
         btn_duplicate.setAttribute('id', 'image_duplic');
         btn_duplicate.setAttribute('src', '/static/base/img/copier-coller-1.png');
         btn_duplicate.setAttribute('width', '25px');
         btn_duplicate.setAttribute('height', '25px');
         // Validation d'une ligne et envoi à l'API
         let btn_Validate = document.createElement('input');
         btn_Validate.setAttribute('type', 'image');
         btn_Validate.setAttribute('id', 'image_Validate');
         btn_Validate.setAttribute('src', '/static/base/img/valider.png');
         btn_Validate.setAttribute('onclick', 'update_send(constraints,parameters)');
         btn_Validate.setAttribute('width', '25px');
         btn_Validate.setAttribute('height', '25px');
         duplic.appendChild(btn_duplicate);
         duplic.appendChild(btn_Validate);

         row.appendChild(duplic);

         //ajout de la ligne à la table
         tblBody.appendChild(row);
     }
// Ajout de la table générer dans la zone HTML
     tbl.appendChild(tblBody);

     consZone.appendChild(tbl);
 }
refresh_param();
        create_menu();
//Fonction transformant un string en un chemin utilisable pour parcourir une liste et/ou un objet JS
function stringGetter (getter) {
        return getter
        .split('.')
        .reduce((o,i)=>o[i], parameters);
      }


/**
 * Suppression d'un paramètre
 * @param param
 *
 */
function suppr(param){
    param.length=0;
    document.getElementById('tableBody').remove();
    //Regéneration des lignes de contraintes
    refresh_param();
    // Création des nouvaux menus déroulant
    create_menu();
}


/**
 * Activation/désactivation d'un paramètre
 * @param param
 *
 */
function activate(checkbox,param){
      if (checkbox.checked) {
                param.is_active = true;
                console.log(param.is_active);
            }
            else {
                param.is_active = false;
                console.log(param.is_active);
            }

}

/**
 * Gestion du poids d'une contrainte
 * @param slider, param
 *
 *
 */
function update_weight(slider,param){
    param.weight = slider.value;
}

/**
 * Envoi de la contrainte modifié à l'API
 * @param constr,param
 *
 *
 */
function update_send(constr,param){
   console.log(constr);
   console.log(param);
}


/**
 * Cacher/afficher un élement
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


// Fonction permettant la génération du menu déroulant des options
function create_menu() {
    for (let cpt = 0; cpt < constraints.length; cpt++) {
        var ldd = document.getElementById("ChoixP" + cpt);

        //Création du menu option que l'on rempli.
        for (let j = 0; j < constraints[cpt].parameters.length; j++) {
            if (constraints[cpt].parameters[j].id_list.length == 0) {
                var opt = document.createElement('option');
                opt.innerHTML = constraints[cpt].parameters[j].name;
                ldd.appendChild(opt);
            }
        }

        // Javascript du menu déroulant permettant la sélection
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


// Listener permettant de retourner les elements selectionner dans le easyselect
        $('#valider' + cpt).click(function () {
            $('#ChoixP' + cpt + ' option:selected').each(function () {
                str = $(this).text() + " ";
                val = $(this).val();
                console.log(str, val);
            })
        });

    }
}





