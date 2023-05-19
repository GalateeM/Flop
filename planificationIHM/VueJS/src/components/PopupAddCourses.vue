<template>
    <div>
        <div class="background" />
        <div class="window">
            <MainTitle value="Ajouter des cours" />
            <CloseButton @click.native="$parent.popupVisible = false; edit = -1" />
            <div class="container">
                <div v-if="homeScreen">
                    <li v-for="(course, key) in savedCourses" :key="key" class="vertical-list">
                        <HorizontalBanner :value="resumeCourse(savedCourses[key])" color="#2A27D8"
                            @delete="savedCourses.splice(key, 1)" @edit="editCourse(key)" />
                    </li>
                    <HorizontalBannerSimple @click.native="setHomeScreen(false)" value="+" color="#2A27D8" />
                    <div class="buttons">
                        <SimpleButton value="Enregistrer" color="#05B12B" @click.native="$parent.popupVisible = false" />
                    </div>
                </div>
                <div v-else>
                    <div id="week-numbers">
                        <li v-for="week in weeks" :key="week" class="horizontal-list">
                            <WeekNumber :number=week
                                @value="v => v > 0 ? $set(course.weeks, week, v) : $delete(course.weeks, week)" />
                        </li>
                    </div>
                    <div id="forms">
                        <SimpleInput class="form-element" label="Module" :options="modules" edit="module"
                            @value="v => $set(course, 'module', v)" />
                        <MultipleInput class="form-element" label="Groupe(s)" :options="groups" edit="groups"
                            @value="v => $set(course, 'groups', v)" />
                        <MultipleInput class="form-element" label="Professeur(s)" :options="teachers" edit="teachers"
                            @value="v => $set(course, 'teachers', v)" />
                        <SimpleInput class="form-element" label="Type de cours" :options="courseTypes" edit="courseType"
                            @value="v => $set(course, 'courseType', v)" />
                        <SimpleInput class="form-element" label="Type de salle" :options="roomTypes" edit="roomType"
                            @value="v => $set(course, 'roomType', v)" />
                    </div>
                    <div class="buttons">
                        <SimpleButton value="Annuler" color="#E90B0B" @click.native="homeScreen = true; edit = -1" />
                        <SimpleButton value="Valider" color="#05B12B" @click.native="saveCourse" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import MainTitle from './MainTitle.vue'
import CloseButton from './CloseButton.vue'
import HorizontalBanner from './HorizontalBanner'
import HorizontalBannerSimple from './HorizontalBannerSimple.vue'
import WeekNumber from './WeekNumber.vue'
import SimpleButton from './SimpleButton.vue'
import SimpleInput from './SimpleInput.vue'
import MultipleInput from './MultipleInput.vue'
import flopUrl from '../main.js'

export default {
    name: 'PopupAddCourses',
    components: {
        MainTitle,
        CloseButton,
        HorizontalBanner,
        WeekNumber,
        SimpleButton,
        SimpleInput,
        MultipleInput,
        HorizontalBannerSimple
    },
    data() {
        return {
            routes: {
                "modules": "courses/module/",
                "teachers": "fetch/idtutor",
                "groups": "groups/structural/",
                "roomTypes": "fetch/idroomtype/",
                "courseTypes": "fetch/idcoursetype/"
            },
            homeScreen: true,
            edit: -1,
            weeks: [...Array(52).keys()].map(e => e + 1),
            savedCourses: [],
            course: {
                weeks: {}
            }
        }
    },
    methods: {
        setHomeScreen(show) {
            this.homeScreen = show;
        },
        saveCourse() {
            if (this.edit === -1) this.savedCourses.push(this.course);
            else this.savedCourses[this.edit] = this.course
            this.setHomeScreen(true);
            this.course = {
                weeks: {}
            };
            this.edit = -1;
        },
        editCourse(key) {
            this.course = this.savedCourses[key];
            this.edit = key;
            this.setHomeScreen(false);
        },
        optionsToString(ids, options) {
            return ids.map(id => options.find(o => o.id == id).name).join(", ");
        },
        resumeCourse(course) {
            //TODO: change 90 by real data
            let minutes = Object.values(course.weeks).reduce((a, b) => a + b, 0) * 90;
            let time = Math.floor(minutes / 60) + "h" + ((minutes % 60) >= 10 ? (minutes % 60) : "0" + (minutes % 60));
            let weeks = Object.keys(course.weeks).join(", ");
            let groups = course.groups ? this.optionsToString(course.groups, this.groups) : "aucun";
            let module = course.module ? this.optionsToString([course.module], this.modules) : "aucun";
            let teachers = course.teachers ? this.optionsToString(course.teachers, this.teachers) : "aucun";
            let courseType = course.courseType ? this.optionsToString([course.courseType], this.courseTypes) : "aucun";
            let roomType = course.roomType ? this.optionsToString([course.roomType], this.roomTypes) : "aucune";
            return `${time} ➔ Semaines: ${weeks} | Module: ${module} | Groupes: ${groups} | Professeurs: ${teachers} | Cours: ${courseType} | Salle: ${roomType}`
        },
        async fetchJson(url) {
            const res = await fetch(url)
            const data = res.json();
            return data;
        },
        fetchAllData(dept, apiUrl, routes) {
            let data = [];
            Object.keys(routes).forEach(async key => {
                data.push(this.fetchJson(apiUrl + routes[key] + "?dept=" + dept));
            });
            return data;
        }
    },
    mounted() {
        let proms = this.fetchAllData("HES3", flopUrl, this.routes);
        Promise.all(proms).then(res => {
            console.log(res)
            this.modules = res[Object.keys(this.routes).indexOf("modules")].map(e => { return { "id": e.abbrev, "name": e.name } });
            this.teachers = res[Object.keys(this.routes).indexOf("teachers")];
            this.groups = res[Object.keys(this.routes).indexOf("groups")].map(e => { return { "id": e.id, "name": e.name } });
            this.courseTypes = res[Object.keys(this.routes).indexOf("courseTypes")];
            this.roomTypes = res[Object.keys(this.routes).indexOf("roomTypes")];
        })/*
        this.modules = data.modules.map(e => { return { "id": e.abbrev, "name": e.name } });
        this.teachers = data.teachers;
        this.groups = data.groups.map(e => { return { "id": e.id, "name": e.name } });
        this.courseTypes = data.courseTypes;
        this.roomTypes = data.roomTypes;*/
    }
}
</script>

<style scoped>
.background {
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 100%;
    background-color: black;
    opacity: 70%;
}

.window {
    text-align: left;
    overflow-y: auto;
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    margin-top: 5%;
    margin-bottom: 5%;
    margin-left: 10%;
    margin-right: 10%;
    background-color: #D9D9D9;
    opacity: 100%;
    border-radius: 20px;
}

.container {
    margin-top: 5%;
}

.buttons {
    position: absolute;
    bottom: 0;
    right: 0;
    left: 0;
    text-align: center;
}

.horizontal-list {
    list-style-type: none;
    display: inline-block;
    margin: auto;
    padding-left: 0.2em;
    padding-right: 0.2em;
}

.vertical-list {
    list-style-type: none;
}

.edit-delete {
    position: absolute;
}

#week-numbers {
    padding-left: 1em;
    padding-bottom: 1em;
    overflow: auto;
    white-space: nowrap;
}

#forms {
    margin-left: 1em;
    margin-right: 1em;
    margin-top: 1em;
}

.form-element {
    vertical-align: top;
    display: inline-block;
    margin-right: 8em;
    margin-bottom: 2em;
}
</style>