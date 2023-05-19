<template>
    <!--Componant Prof-->
    <div class="Prof" >
        <p class="ProfName" @mouseover="showFullGroupName"  @mouseout="hideFullGroupName">{{ProfName}}</p>
        <!--Creation of all the Cours that corresponds to this Prof-->
        <div v-for="(cours, index) in listeCours" :key="index">
            <Cours :salle="cours.salle" :date="cours.day" :module="cours.titre" :prof="cours.prof" :groupe="cours.groupe" :heure="cours.heure" :duree="cours.duree" :color="cours.color" :nbCoursOnThisTime="cours.nbCoursOnThisTime"/>
        </div>
    </div>
</template>

<script>
import Cours from './Cours.vue';
import { getCoursByProf } from "./main.js";

export default{
    name : 'Prof',
    components:{ 
        Cours 
    },

    props :{ 
        ProfName:String,
        nbweek: Number
    },

    data() {
        return {
            listeCours: [],
        };
    },


    created(){
            this.listeCours = getCoursByProf(this.ProfName,this.nbweek);
    },
    methods :{
    
        //Function to Show the name of the prof. It useful when there is a lot of Prof/Groups
        showFullGroupName(event) {
            // Récupère le texte complet du groupe
            const fullGroupName = this.ProfName;
            // Crée un élément div pour afficher le nom complet sous la souris
            const tooltip = document.createElement('div');
            tooltip.classList.add('tooltip');
            tooltip.textContent = fullGroupName;
            // Ajoute le tooltip à la page
            document.body.appendChild(tooltip);
            // Positionne le tooltip sous la souris
            const x = event.pageX + 10;
            const y = event.pageY + 10;
            tooltip.style.left = `${x}px`;
            tooltip.style.top = `${y}px`;
        },

        hideFullGroupName() {
            // Supprime l'élément div contenant le nom complet du groupe
            const tooltip = document.querySelector('.tooltip');
            if (tooltip) {
                document.body.removeChild(tooltip);
            }
        },

    },
};
</script>


<style>


.ProfName{

        margin: 0;
        font-size: 12px; /* par exemple, ajustez selon vos besoins */
        text-align: center;
        white-space: nowrap; /* empêche le texte de passer à la ligne */
        overflow: hidden; /* cache le texte qui dépasse */
        text-overflow: ellipsis; /* ajoute des points de suspension à la fin du texte caché */
    
}

</style>