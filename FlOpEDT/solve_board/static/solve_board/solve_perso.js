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
let parameters = {
    people:{
        Tutor:[
            {id:1,username:'PSE'}

        ]
    },
    base:{
        Module:[
            {id:1,abbrev:'AMN'}

        ]
    }
}

let constraints = [
        {
        id: 8, // id de la TTC
        name: "Covoiturage", // nom du type de TTC
        weight: 1, // poids de la TTC
        is_active: true, // contrainte active ?
        category : 2, // Id de la catégorie
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
            id_list: [1], // ids des objets pour le paramètre dans la TTC
            acceptable: [1,2,3,4] // ids des objets acceptables comme valeur du paramètre
            },
            {
            name: "Module", // nom du paramètre dans la TTC
            type: 'base.Module', // nom du type des objets dans ce paramètre
            required: false, // paramètre obligatoire ?
            all_except: true, // tous sauf ?
            multiple : false,
            id_list: [], // ids des objets pour le paramètre dans la TTC
            acceptable: [5,6,7,8] // ids des objets acceptables comme valeur du paramètre
            },
            {
            name: "Eleve", // nom du paramètre dans la TTC
            type: 'base.Student', // nom du type des objets dans ce paramètre
            required: false, // paramètre obligatoire ?
            all_except: true, // tous sauf ?
            multiple : false,
            id_list: [5], // ids des objets pour le paramètre dans la TTC
            acceptable: [5,6,7,8] // ids des objets acceptables comme valeur du paramètre
            }
        ]
    },
    {
        id: 9, // id de la TTC
        name: "Random", // nom du type de TTC
        weight: 2, // poids de la TTC
        is_active: false, // contrainte active ?
        comment: "", // commentaire sur la TTC
        last_modification: null, // date de création
        weeks : [{nb: 14 , year: 2021},{nb: 33 , year: 2021}], // week a la forme : {nb: int , year: int}
        parameters : [
            {
            name: "Lettre", // nom du paramètre dans la TTC
            type: "str", // nom du type des objets dans ce paramètre
            required: true, // paramètre obligatoire ?
            all_except: true, // tous sauf ?
            multiple : false,
            id_list: ["A"], // ids des objets pour le paramètre dans la TTC
            acceptable: ["A","B"] // ids des objets acceptables comme valeur du paramètre
            },
            {
            name: "Nombres", // nom du paramètre dans la TTC
            type: 'int', // nom du type des objets dans ce paramètre
            required: false, // paramètre obligatoire ?
            all_except: true, // tous sauf ?
            multiple : true,
            id_list: [], // ids des objets pour le paramètre dans la TTC
            acceptable: [1,7,6,8,9] // ids des objets acceptables comme valeur du paramètre
            },
            {
            name: "Eleve", // nom du paramètre dans la TTC
            type: 'base.Student', // nom du type des objets dans ce paramètre
            required: false, // paramètre obligatoire ?
            all_except: true, // tous sauf ?
            multiple : false,
            id_list: [5], // ids des objets pour le paramètre dans la TTC
            acceptable: [5,6,7,8] // ids des objets acceptables comme valeur du paramètre
            }
        ]
    },
    {
        id: 9, // id de la TTC
        name: "Bonsoir", // nom du type de TTC
        weight: 8, // poids de la TTC
        is_active: true, // contrainte active ?
        comment: "", // commentaire sur la TTC
        last_modification: null, // date de création
        weeks : [{nb: 14 , year: 2021},{nb: 33 , year: 2021}], // week a la forme : {nb: int , year: int}
        parameters : [
            {
            name: "Lettre", // nom du paramètre dans la TTC
            type: "str", // nom du type des objets dans ce paramètre
            required: false, // paramètre obligatoire ?
            all_except: true, // tous sauf ?
            multiple : false,
            id_list: ["A"], // ids des objets pour le paramètre dans la TTC
            acceptable: ["A","B"] // ids des objets acceptables comme valeur du paramètre
            },
            {
            name: "Nombres", // nom du paramètre dans la TTC
            type: 'int', // nom du type des objets dans ce paramètre
            required: false, // paramètre obligatoire ?
            all_except: true, // tous sauf ?
            multiple : true,
            id_list: [1,7], // ids des objets pour le paramètre dans la TTC
            acceptable: [1,7,6,8,9] // ids des objets acceptables comme valeur du paramètre
            },
            {
            name: "horaire", // nom du paramètre dans la TTC
            type: 'int', // nom du type des objets dans ce paramètre
            required: false, // paramètre obligatoire ?
            all_except: true, // tous sauf ?
            multiple : true,
            id_list: [], // ids des objets pour le paramètre dans la TTC
            acceptable: [1,7,6,8,9] // ids des objets acceptables comme valeur du paramètre
            }

        ]
    }];




//Variables



let consZone = document.getElementById("Zone de contrainte");
let tbl = document.createElement("table");
let tblBody = document.createElement("tbody");
let parametres;

//Boucle parcourant chaque contrainte 1 par 1
for (let l = 0; l < lines.length; l++) {



    // creation d'une colonne
    let row = document.createElement("tr");
        row.setAttribute('class','ligne_contrainte')

    // Bouton sélection

    let select = document.createElement("td");
        select.setAttribute('class','selec_contrainte')
    let selec = document.createElement('input');
    selec.setAttribute('type', 'checkbox');
    selec.setAttribute('id', 'selection');
    selec.setAttribute('name', 'selection');
    select.appendChild(selec);
    row.appendChild(select);
    if (lines[l].is_active === true) {
        selec.checked = true;
    }


    //Nom de la contrainte
    let div_nom = document.createElement("td");
        div_nom.setAttribute('class','nom_contrainte');
    nom = document.createTextNode(lines[l].name);
    div_nom.appendChild(nom);
    row.appendChild(div_nom);

// Parametres de la contraintes
let para = document.createElement("td");
    para.setAttribute('class','para_contrainte')
let ol = document.createElement("ol");
let p = document.createElement("p");
    //Les différents parametres existants de la ligne de contrainte
    for (let k = 0; k < lines[l].parameters.length; k++) {
    let btn_Possib = document.createElement('input');
    btn_Possib.setAttribute('type', 'image');
    btn_Possib.setAttribute('id', 'image_Add');
    btn_Possib.setAttribute('src', '/static/base/img/ajout.png');
    btn_Possib.setAttribute('width', '15px');
    btn_Possib.setAttribute('height', '15px');

    let btn_Suppr = document.createElement('input');
    btn_Suppr.setAttribute('type', 'image');
    btn_Suppr.setAttribute('id', 'image_Add');
    btn_Suppr.setAttribute('src', '/static/base/img/suppression.png');
    btn_Suppr.setAttribute('width', '15px');
    btn_Suppr.setAttribute('height', '15px');
        let li = document.createElement("li");
        if(lines[l].parameters[k].id_list.length!=0){
            parametres = document.createTextNode("  "+lines[l].parameters[k].name+"  ");
            if(lines[l].parameters[k].required===true){
            li.appendChild(parametres);
            li.appendChild(btn_Suppr);
            ol.appendChild(p);
            ol.appendChild(li);
            }else{
                li.appendChild(btn_Possib);
                li.appendChild(parametres);
                li.appendChild(btn_Suppr);
                ol.appendChild(p);
                ol.appendChild(li);
            }
        }
        para.appendChild(ol);
    }
    row.appendChild(para);

    //Bouton permettant l'affichage du menu déroulant
    let ajout_Param = document.createElement("td");
        ajout_Param.setAttribute('class','ajout_param');
    let btn = document.createElement('input');
    btn.setAttribute('type', 'image');
    btn.setAttribute('id', 'image_Add');
    btn.setAttribute('src', '/static/base/img/ajout.png');
    btn.setAttribute('width', '25px');
    btn.setAttribute('height', '25px');
    btn.setAttribute('onclick', 'hide'+l+'()');
    ajout_Param.appendChild(btn);
    row.appendChild(ajout_Param);

    //Ajout de la zone permettant l'affichage du menu déroulant
    let Menu = document.createElement("div");
    Menu.setAttribute('id', 'Menu'+l);
    let Select = document.createElement("select");
    Select.setAttribute('id', 'ChoixP'+l);
    Select.setAttribute('data-max', '');
    Select.setAttribute('multiple', 'multiple');
    Select.setAttribute('style', '');
    Menu.appendChild(Select);
    ajout_Param.appendChild(Menu);
    row.appendChild(ajout_Param);

    //Activation d'une ligne
    let activ = document.createElement("td");
        activ.setAttribute('class','activ_contrainte');
    let activate = document.createElement('input');
    activate.setAttribute('type', 'checkbox');
    activate.setAttribute('id', 'activation');
    activate.setAttribute('name', 'activation');
    activ.appendChild(activate);
    row.appendChild(activ);

// Selection du poids
let range_td = document.createElement("td");
    range_td.setAttribute('class','poid_contrainte');

let slide_div = document.createElement('div');
    slide_div.setAttribute('class','range-slider')

let slide_btn = document.createElement('input');
    slide_btn.setAttribute('type', 'range');
    slide_btn.setAttribute('min', '1');
    slide_btn.setAttribute('max', '8');
    slide_btn.setAttribute('value', lines[l].weight);
    slide_btn.setAttribute('class', 'range-slider__range');
    slide_btn.setAttribute('id', 'Weight');
    slide_btn.setAttribute('name', 'Weight');
let spans = document.createElement("span");
    spans.setAttribute('class','range-slider__value');
    spans.textContent = lines[l].weight;
    slide_div.appendChild(slide_btn);
    range_td.appendChild(slide_div);
    slide_div.appendChild(spans);
    row.appendChild(range_td);



// Duplication
let duplic = document.createElement("td");
    duplic.setAttribute('class','duplic_contrainte');
    let btn_duplicate = document.createElement('input');
    btn_duplicate.setAttribute('type', 'image');
    btn_duplicate.setAttribute('id', 'image_duplic');
    btn_duplicate.setAttribute('src', '/static/base/img/copier-coller-1.png');
    btn_duplicate.setAttribute('width', '25px');
    btn_duplicate.setAttribute('height', '25px');
    duplic.appendChild(btn_duplicate);
    row.appendChild(duplic);

    // add the row to the end of the table body
    tblBody.appendChild(row);

}


tbl.appendChild(tblBody);
consZone.appendChild(tbl);




//*************************************************************************
var ldd0 = document.getElementById("ChoixP0");

        for(let j0 =0;j0<lines[0].parameters.length;j0++){
            if(lines[0].parameters[j0].id_list.length==0 ) {
                var opt0 = document.createElement('option');
                opt0.innerHTML = lines[0].parameters[j0].name;
                ldd0.appendChild(opt0);
            }
        }

$("#ChoixP0").easySelect({
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

document.getElementById("Menu0").style.display = "none";
     function hide0() {
        let x = document.getElementById("Menu0");
        if (x.style.display === "none") {
            x.style.display = "block";
        } else {
            x.style.display = "none";
        }
    }
//*************************************************************************


//*************************************************************************
var ldd1 = document.getElementById("ChoixP1");

        for(let j1 =0;j1<lines[1].parameters.length;j1++){
            if(lines[1].parameters[j1].id_list.length==0){
             var opt1 = document.createElement('option');
             opt1.innerHTML = lines[1].parameters[j1].name;
             ldd1.appendChild(opt1);
            }
        }

$("#ChoixP1").easySelect({
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

document.getElementById("Menu1").style.display = "none";
     function hide1() {
        let x = document.getElementById("Menu1");
        if (x.style.display === "none") {
            x.style.display = "block";
        } else {
            x.style.display = "none";
        }
    }
//*************************************************************************


//*************************************************************************
var ldd2 = document.getElementById("ChoixP2");

        for(let j2 =0;j2<lines[2].parameters.length;j2++){
            if(lines[2].parameters[j2].id_list.length==0 ) {
                var opt2 = document.createElement('option');
                opt2.innerHTML = lines[2].parameters[j2].name;
                ldd2.appendChild(opt2);
            }
        }

$("#ChoixP2").easySelect({
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

document.getElementById("Menu2").style.display = "none";
     function hide2() {
        let x = document.getElementById("Menu2");
        if (x.style.display === "none") {
            x.style.display = "block";
        } else {
            x.style.display = "none";
        }
    }
//*************************************************************************


//*************************************************************************
var lddopt = document.getElementById("ChoixPOpt");

        for(let j3 =0;j3<lines[1].parameters.length;j3++){
             for(let k2=0;k2<lines[1].parameters[j3].acceptable.length;k2++){
                 var optopt = document.createElement('option');
             optopt.innerHTML = lines[1].parameters[j3].acceptable[k2];
             lddopt.appendChild(optopt);
             }
        }

$("#ChoixPOpt").easySelect({
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

document.getElementById("MenuOpt").style.display = "none";
     function hide_opt() {
        let x = document.getElementById("MenuOpt");
        if (x.style.display === "none") {
            x.style.display = "block";
        } else {
            x.style.display = "none";
        }
    }
//*************************************************************************




