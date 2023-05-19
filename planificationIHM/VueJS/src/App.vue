
<template>
        <!--LE COMPOSANT APP EST LE PRINCIPALE C'EST LUI QUI APPELE LES AUTRES-->
  <div id="app">
    
    <!--Boutton pour accéder à l'ajout des cours-->
    <div id="add-course-button">
      <SimpleButton @click.native="popupVisible=true" value="Ajouter" color="#2A27D8" size="15px" />
    </div>

    <div id="Choice">

      <!--FILTER are not implemented for the moment-->
      <div id="ChooseFilter">    
        <p>Filtre</p> 
        <button>Groupe</button>
        <button>Professeur</button>
        <button>Module</button>
      </div>

      <!--Allow to choose the way to display (by teacher or by group)-->
      <div id="ChooseDisplay">
        <button :class="ShowGroupe ? 'active' : 'inactive'" @click="ShowGroupe = true; ShowProf = false;">Groupe</button>
        <button :class="ShowProf ? 'active' : 'inactive'" @click="ShowGroupe = false; ShowProf = true;">Professeur</button>
        <p>Affichage</p>  
      </div>
  
    </div>

    <!--Buttons to change the weeks to dipslay-->
    <div class="button-container">
           <!--If you want to change the gap when we click on one of the button : Change -2 and 2 in getlistWeek()--> 
      <button class="custom-button" @click="listeWeek = getlistWeek(-2)">&lt;</button>
      <button class="custom-button" @click="listeWeek = getlistWeek(2)">></button>
    </div>

    <!--Creation of all the composants week to display-->
    <div class="weeks">
      <Week class="main" v-for="i in listeWeek" :key="i" :nbweek="i" :ShowGroupe="ShowGroupe" :ShowProf="ShowProf"></Week>
    </div>

    <PopupAddCourses v-if="popupVisible" />
  </div>
</template>


<script>
import Week from './Week.vue';
import "./main.js"
import SimpleButton from './components/SimpleButton.vue'
import PopupAddCourses from './components/PopupAddCourses.vue'

export default {
  name: 'App',
  components: {
    Week,
    SimpleButton,
    PopupAddCourses
  },

  data() {
    return {
      //ShowGroupe, ShowProf, popupVisible are booleans that permits to choose what is currently displaying
      ShowGroupe: false,
      ShowProf: false,
      popupVisible: false,
      //listWeek is a list of number corresponding to all the week number to display. Ex: [19,20,21,22,23,24]
      listeWeek : []
    };
  },

  created(){
    //Init of listeWeek
    setTimeout(() => {
      this.listeWeek = this.getlistWeek(0);
        }, 1000);
     
  },

  methods :{

    //Methods that allows to return the listWeek
    getlistWeek(delay){
      let currentWeek = 0;

      console.log(this.listeWeek)

      if(this.listeWeek.length === 0){
        currentWeek = new Date().getWeek();
      }
      else{
        currentWeek = this.listeWeek[4] + delay;
      }


      const weekList = [];
      //If you want to display more week : change the stop limit condition
      for (let i = currentWeek - 4; i <= currentWeek + 1; i++) {
         weekList.push(i);
      }
      return weekList;
    },

  },

};

</script>

<style>

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

#Choice {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

#ChooseFilter, #ChooseDisplay {
  display: flex;
  align-items: center;
  background-color: #D9D9D9;
  border-radius: 10px;
  margin: 10px;
}

#ChooseDisplay .inactive, #ChooseFilter button{
  font-size: 16px;
  color: #fff;
  background-color: #058f2c;
  border: none;
  padding: 10px 20px;
  margin: 0 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease-in-out;
  border-color: #058f2c;
  border-style: solid;
}

.active{
  font-size: 16px;
  color: #fff;
  background-color: #51e583;
  border: none;
  padding: 10px 20px;
  margin: 0 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease-in-out;
  border-color: #058f2c;
  border-style: solid;
}

#ChooseDisplay p, #ChooseFilter p {
  margin: 0;
  padding: 17px;
}

#ChooseDisplay button:hover,#ChooseFilter button:hover {
  background-color: #29b959;
}

#ChooseFilter {
  margin-right: auto;
}

.weeks {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-evenly;
  align-items: center;
  background-color: #D9D9D9;
}

.weeks .main {
  margin-bottom: 20px;
}

#add-course-button {
  text-align: left;
}


.custom-button {
  display: inline-block;
  padding: 5px 10px;
  margin-bottom: 6px;
  font-size: 14px;
  font-weight: bold;
  text-align: center;
  text-decoration: none;
  border-radius: 90px;
  border-color: #058f2c;
  border-style: solid;
  color: #fff;
  background-color: #058f2c;
  cursor: pointer;
  transition: all 0.3s ease-in-out;
}

.custom-button:hover {
  background-color: #29b959;
}
</style>
