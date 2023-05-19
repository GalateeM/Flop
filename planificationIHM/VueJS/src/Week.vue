<template>
    <div class="week" :id="nbweek">
        <p class="numberoftheweek">SEMAINE {{nbweek}}</p>
        <div class="theweek">
            <div v-for="groupe in listeGroupe" class="ByGroup" v-if="ShowGroupe">
                <Groupe :GroupeName="groupe" :nbweek="nbweek"></Groupe>
            </div>
            <div v-for="prof in listeProf"  class="ByProf" v-if="ShowProf" >
                <Prof :ProfName="prof" :nbweek="nbweek"></Prof>
            </div>
        </div>
    </div>
</template>

<script>
import Groupe from './Groupe.vue';
import Prof from './Prof.vue';
import { getCourse,getListeGroupe,getListeProf } from "./main.js";


export default{

    name: 'Week',
    components : {
        Groupe,
        Prof
    },
    props:{
        nbweek:Number,
        ShowGroupe:Boolean,
        ShowProf:Boolean
    },

    data(){
        return {
            listeGroupe: [""],
            listeProf: [""],
        }
    },

    created(){
        setTimeout(() => {
            this.fetchData();
        },500);
    },

    methods:{
      async fetchData() {
        const courseData = await getCourse(this.nbweek,"2023","HES3");
        this.listeProf= getListeProf(courseData,this.nbweek);
        this.listeGroupe = getListeGroupe(courseData,this.nbweek);
    }
    }


}
</script>

<style>


.week{
    background-color: #B3B3B3;
    height: 250px;
    width: 450px;
    flex: 0 0 450px; /* Ajout d'une règle pour fixer la largeur des blocs à 450px */
    margin : 5px;
    box-sizing: border-box; /* Empêcher l'ajout de padding ou de bordure pour modifier la taille des blocs */
}

.week:nth-child(3n+1) {
    clear: both;
}

.numberoftheweek{
    text-align: left;
    margin: 10px;
    padding-top: 10px;
}
.theweek {
    height: 220px;
    display: flex;
  }
  
.theweek > div {
    flex: 1;
}


.week {
    position: relative;
}
  

  
</style>
