import Vue from 'vue'
import App from './App.vue'
import "regenerator-runtime/runtime";
import vClickOutside from 'v-click-outside'

Vue.use(vClickOutside);

new Vue({
  el: '#app',
  render: h => h(App)
})

//TODO: mettre à jour l'URL
const flopUrl = "http://localhost/fr/api/"
export default flopUrl

//URL Pour recupérer les données de l'API
const URL = flopUrl + "fetch/scheduledcourses/?week="


//Fonction faisant appel à l'API
export async function getCourse(NumberOfTheWeek,year,dept){
  let res = await fetch(URL+NumberOfTheWeek+"&year="+year+"&dept="+dept);
  res = res.json();
  return res ;
}






//FONCTION POUR LES PROFS

//Tableau qui va stocker l'ensemble des cours Stocké pour chaque professeur
let CoursByProf = {};

//Fonction permettant de récupérer la liste de tout les profs 
export function getListeProf(data,NumberOfTheWeek){
  console.log(data)
  let ListeProf = [];
  data.forEach(element => {
    if(!ListeProf.includes(element.tutor)){
      ListeProf.push(element.tutor)
    }
  });
  regrouperCoursParProf(data,NumberOfTheWeek);
  return ListeProf;
}


//Fonction qui permet de remplir le tableau CoursByProf
function regrouperCoursParProf(cours,NumberOfTheWeek) {
  const resultat = {};

  cours.forEach(c => {
    const prof = c.tutor;

    if (!(prof in resultat)) {
      resultat[prof] = [];
    }
    resultat[prof].push({
      titre: c.course.module.name,
      prof: prof,
      groupe: c.course.groups[0].name,
      heure: convertirTempsEnHeureString(c.start_time),
      duree: 1,
      salle : c.room.name,
      color: c.course.module.display.color_bg,
      nbCoursOnThisTime: 0,
      day: getDateFromWeekdayYearWeek(c.day,c.course.year,c.course.week)
    });
  });
  console.log(CoursByProf)
  CoursByProf[NumberOfTheWeek] = resultat;
}

//Fonction renvoyant les cours d'un prof pour une semaine.
export function getCoursByProf(ProfName,NbWeek){
  return (CoursByProf[NbWeek][ProfName]);
}





//FONCTION POUR LES GROUPES 


//Tableau qui va stocker l'ensemble des cours Stocké pour chaque groupe
let CoursByGroupe = {};

//Fonction permettant de récupérer la liste de tout les Groupe
export function getListeGroupe(data,NbWeek){

  let ListeGroupe = [];
  data.forEach(element => { 
    if(!ListeGroupe.includes(element.course.groups[0].name)){
      ListeGroupe.push(element.course.groups[0].name);
    }
  });
  regrouperCoursParGroupe(data,NbWeek)
  return ListeGroupe;
}

//Fonction qui permet de remplir le tableau CoursByGroupe
function regrouperCoursParGroupe(cours,NumberOfTheWeek) {
  const resultat = {};

  cours.forEach(c => {
    const groupe =  c.course.groups[0].name;

    if (!(groupe in resultat)) {
      resultat[groupe] = [];
    }
    resultat[groupe].push({
      titre: c.course.module.name,
      prof: c.tutor,
      groupe: c.course.groups[0].name,
      heure: convertirTempsEnHeureString(c.start_time),
      duree: 1,
      color: c.course.module.display.color_bg,
      nbCoursOnThisTime: 0,
      salle : c.room.name,
      day: getDateFromWeekdayYearWeek(c.day,c.course.year,c.course.week)
    });
  });
  CoursByGroupe[NumberOfTheWeek] = resultat;
}

//Fonction renvoyant les cours d'un groupe pour une semaine.
export function getCoursByGroupe(GroupeName,NbWeek){
  return (CoursByGroupe[NbWeek][GroupeName]);
}


//Fonction qui renvoi le numero du jours dans la semaine a partir des initiales du jour
function getDayNumber(day) {
  const daysOfWeek = ["su", "m", "tu", "w", "th", "f", "sa"];
  return daysOfWeek.indexOf(day);
}


//Fonction pour obtenir une date de type : "Vendredi 19 Mai 2023", a partir du jour de la semaine, l'année et le numéro de semaine)
function getDateFromWeekdayYearWeek(dayOf, year, week) {
  const weekday = getDayNumber(dayOf);
  const date = new Date(year, 0, 1 + (week - 1) * 7);
  const day = date.getDay();
  const diff = (weekday - day + 7) % 7;
  date.setDate(date.getDate() + diff);
  const options = { weekday: "long", day: "numeric", month: "long", year: "numeric" };
  return date.toLocaleDateString("fr-FR", options);
}

//Modif du prototype Date de JS pour lui ajouter la fonction getWeek qui retourner le numero de semaine d'une date
Date.prototype.getWeek = function() {
  const date = new Date(this.getTime());
  date.setHours(0, 0, 0, 0);
  date.setDate(date.getDate() + 4 - (date.getDay() || 7));
  const yearStart = new Date(date.getFullYear(), 0, 1);
  const weekNo = Math.ceil(((date - yearStart) / 86400000 + 1) / 7);
  return weekNo;
};


function convertirTempsEnHeureString(temps) {
  var heures = Math.floor(temps / 60); // Obtient le nombre d'heures
  var minutes = temps % 60; // Obtient le nombre de minutes

  // Formate l'heure et les minutes avec des zéros devant si nécessaire
  var heureString = heures < 10 ? "0" + heures : heures;
  var minuteString = minutes < 10 ? "0" + minutes : minutes;

  // Retourne la chaîne de caractères représentant l'heure
  return heureString + "h" + minuteString;
}




