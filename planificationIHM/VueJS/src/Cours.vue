<template>
    <div class="Cours">
        
        <div class="affich" :style="cssVars" @click="showPopup = !showPopup"></div>

        <!--Class Popup is only displaying when we click on a cours to have more information about this one-->
        <div class="popup" v-if="showPopup">
            <div class="info" >
                <h2 class="Titre"> Module : {{ module }}</h2>
                <p class="Prof"> Professeur : {{ prof }}</p>
                <p class="Groupe"> Groupe : {{ groupe }}</p>
                <p class="Salle"> Salle : {{ salle }}</p>
                <p class="Heure">Heure : {{ heure }}</p>
                <p class="Date">Date : {{ date }}</p>
                <button class="close-button" @click="showPopup = !showPopup">&times;</button>
            </div>
            <!--This class is only use to add the blanck behing when we click on a Cours componant-->
            <div class="overlay"></div>
        </div>

    </div>
</template>

<script>
export default{
    name : 'Cours',
    data(){
        return{
            showPopup : false,
        }
    },
    props: {
        module: String,
        prof: String,
        groupe: String,
        heure: String,
        duree: Number,
        color: String,
        date : String,
        salle : String,
    },
    computed: {

        //If you want to change the way to show a Cours (bigger, smaler ....)
        cssVars () {
            return{
                /* variables you want to pass to css */
                'background-color': this.color,
                'height': this.duree*20 +"px",
                'width' : 90 + "%"/*/ this.nbCoursOnThisTime +"%"*/
    
            }
        }
    },
}

</script>

<style scoped>


.affich{
    margin: auto;
    margin-bottom: 4px ;
}

.info{
  background-color: white;
  border-radius: 5%;
  border : solid;
  border-width:  3px;
  border-color: black;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 50px;
  z-index: 3;
}

.close-button {
    position: absolute;
    top: 5px;
    right: 5px;
    cursor: pointer;
    border-radius: 50%;
    background-color: #ccc;
    color: #fff;
    font-size: 35px;
    text-align: center;
    line-height: 30px;
 }
  
.close-button:hover {
    background-color: #999;
}

.overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(255, 255, 255, 0.8);
    z-index: 2; /* assurez-vous que l'élément a un index z supérieur à celui de votre popup */
}

</style>