
for(let item of allPreferencesItems[name]){
    // Faites les trucs qui créent votre ligne
    // et mettez ces deux lignes à l'endroit qui vous intéresse
    let newBarKiff=document.getElementById(`kiffDegree${name}${item.id}`)
    newBarKiff.innerHTML=addCircles(`${name}Kiff_${item.name}`,`${name}KiffBar_${item.name}`);
    }
for(let elmt of allcircles){
     //The element cirlcle clicked take the attribut check=true
     elmt.addEventListener("click",otherCircleInCheckFalse);
     elmt.addEventListener("click", circleInCheckTrue);

     //animation that put a black border on the circle
     elmt.addEventListener("click",animNull);
     elmt.addEventListener("click", animBorderBlack);
    }


   let circles=[{id:1, color:"#009000", coordx:10,value:8},
{id:2, color:"#40A400" , coordx:30,value:7},
{id:3, color:"#80B800" , coordx:50,value:6},
{id:4, color:"#BFCC00" , coordx:70,value:5},
{id:5, color:"#FFA500" , coordx:90,value:4},
{id:6, color:"#FF7C00" , coordx:110,value:3},
{id:7, color:"#FF5300" , coordx:130,value:2},
{id:8, color:"#FF3000", coordx:150,value:1},
{id:9, color:"#FF0000", coordx:170,value:0}]


function addCircles(idCircle,idBar){
	let newCircles="<g id="+idBar+">";
	for(let c of circles){
			let coordx=c.id*6+50;
			let newCircle= `<g id="`+idCircle+`circleContent${c.id}"> <circle class="circleKiff" id="`+idCircle+`circle${c.id}" cx=${c.coordx} cy=10 r=10 fill="${c.color}" value=${c.value} check="False"> </g>`;
			newCircles=newCircles+newCircle
			// //sens interdit pour le cercle 9
			// if(c.id===9){

			// 	d3.select("#"+idCircle+"circleContent9")
			// 	.append("rect")
			// 	.attr("x",163)
			// 	.attr("y",9)
			// 	.attr("width",14)
			// 	.attr("height",2.5)
			// 	.attr("fill","white");
			// }
	}
	newCircles=newCircles+"</g>";
	return newCircles
}





//allCircles récupère tous les cercles de kiff
//let allcircles=document.getElementsByClassName("circleKiff")

/*####################################Fonctionnel####################################*/

//Quand on click sur un cercle, il prend l'attribut check=True et les autres cercles de sa ligne prennent l'attribut check=False
for(let elmt of allcircles){
	elmt.addEventListener("click",otherCircleInCheckFalse);
	elmt.addEventListener("click", circleInCheckTrue);
}
//Quand on click sur cercle, il prend l'attribut check=True
function circleInCheckTrue(event){
	let circleId=event.originalTarget.id;
	d3.select("#"+circleId).attr("check","True");
}
//Quand on click sur un cercle, les autres prennent l'attribut check=False
function otherCircleInCheckFalse(event){
	console.log(event);
	let idLine=event.target.parentNode.parentNode.id;
	d3.select("#"+idLine).selectAll("circle").attr("check","False");
}

/*####################################Animation####################################*/
//Animation quand on clique sur l'un des cercles

for(let elmt of allcircles){
	elmt.addEventListener("click",animNull);
	elmt.addEventListener("click", animBorderBlack);
}

//fonction qui ajoute un contour noir sur un cercle sélectionné et qui l'enlève si déjà sélectionné
function animBorderBlack(event){
	let circleId=event.originalTarget.id;
	d3.select("#"+circleId).attr("stroke","black").attr("stroke-width",5).attr("r",8);
	let value=event.explicitOriginalTarget.attributes.value.nodeValue;
	if(value==="0"){
		alert("Attention, choisir cette préférence indique un refus total!");
	}
}

//quand on click sur un cercle, les autres sont démunis de leurs animation
function animNull(event){
	let idLine=event.explicitOriginalTarget.parentNode.parentNode.id;
	d3.select("#"+idLine).selectAll("circle").attr("stroke-width",0).attr("r",10);
}

/*########################################################################*/
