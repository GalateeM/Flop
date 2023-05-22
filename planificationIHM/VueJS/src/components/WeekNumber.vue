<template>
    <div class="week-number">
        <div class="circle" @click="toggleSelect"
            :style="selected ? { 'background-color': '#05B12B' } : { 'background-color': 'white' }">
            {{ number < 10 ? "0" + number : number }} </div>
                <div class="arrows">
                    <div class="arrow-left" @click="minus()" />
                    <div class="course-number">{{ courses }}</div>
                    <div class="arrow-right" @click="plus()" />
                </div>
        </div>
</template>

<script>
export default {
    name: 'WeekNumber',
    props: {
        number: Number
    },
    data() {
        return {
            // si  edit est différent de -1 alors on sélectionne la semaine si c'est le cas et on mets le bon nombre de cours 

            selected: this.$parent.edit == -1 ? false : Object.keys(this.$parent.savedCourses[this.$parent.edit].weeks).includes(this.number.toString()),
            courses: this.$parent.edit == -1 || !this.$parent.savedCourses[this.$parent.edit].weeks[this.number] ? 0 : this.$parent.savedCourses[this.$parent.edit].weeks[this.number]        }
    },
    methods: {
        plus() {
            this.courses++;
            if (!this.selected) this.toggleSelect();
            this.$emit("value", this.courses);
        },
        minus() {
            if (this.courses > 0) this.courses--;
            if (this.courses == 0 && this.selected) this.toggleSelect();
            this.$emit("value", this.courses);
        },
        toggleSelect() {
            this.selected = !this.selected;
            this.selected ? this.courses = 1 : this.courses = 0;
            this.$emit("value", this.courses);
        }
    }
}
</script>

<style scoped>
.week-number {
    margin: 0.1em;
    -webkit-user-select: none;
    /* Safari */
    -ms-user-select: none;
    /* IE 10 and IE 11 */
    user-select: none;
    /* Standard syntax */
}

.course-number {
    display: inline-block;
    vertical-align: middle;
    text-align: center;
    font-size: 110%;
    font-weight: bold;
    color: white;
}

.circle {
    text-align: center;
    background-color: white;
    font-size: 150%;
    font-weight: bold;
    padding: 0.3em;
    margin-bottom: 0.2em;

    -moz-border-radius: 50%;
    -webkit-border-radius: 50%;
    border-radius: 50%;
    cursor: pointer;
}

.arrows {
    text-align: center;
    vertical-align: middle;
}

.arrow-right {
    display: inline-block;
    vertical-align: middle;
    width: 0;
    border-top: 0.5em solid transparent;
    border-bottom: 0.5em solid transparent;
    border-left: 0.5em solid white;
    margin: 0.1em;
    margin-left: 0.2em;
    cursor: pointer;
}

.arrow-left {
    display: inline-block;
    vertical-align: middle;
    width: 0;
    height: 0;
    border-top: 0.5em solid transparent;
    border-bottom: 0.5em solid transparent;
    border-right: 0.5em solid white;
    margin: 0.1em;
    margin-right: 0.2em;
    cursor: pointer;
}
</style>