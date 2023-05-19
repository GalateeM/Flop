<template>
    <div>
        <label for="select">{{ label }}</label>
        <select v-show="small" @click="$event => small = false">
            <option selected disabled>{{ optionsToString() }}</option>
        </select>
        <select class="unwrapped" name="select" multiple size="6" v-if="!small" v-click-outside="$event => small = true"
            v-model="selectedOptions" @change="$emit('value', selectedOptions)">
            <option disabled class="help">ctrl/cmd + clic</option>
            <option v-for="option in options" :key="option.id" :value="option.id" :selected="option.id == 'a'">{{
                option.name
            }}</option>
        </select>
    </div>
</template>

<script>
export default {
    name: 'MultipleInput',
    props: ['label', 'options', 'edit'],
    data() {
        return {
            small: true,
            selectedOptions: []
        }
    },
    methods: {
        optionsToString() {
            if (this.$parent.edit != -1 && this.$parent.savedCourses[this.$parent.edit][this.edit]) return this.$parent.savedCourses[this.$parent.edit][this.edit].map(id => this.options.find(o => o.id == id).name).join(", ")
            else return this.selectedOptions.map(id => this.options.find(o => o.id == id).name).join(", ");
        }
    }

}
</script>

<style scoped>
div {
    width: 15rem;
}

.unwrapped {
    position: absolute;
    width: 15rem;
}

.help {
    font-weight: normal;
    margin-bottom: 0.5em;
}

label {
    width: 100%;
    display: block;
    font-weight: bold;
    margin-bottom: 0.2em;
    margin-left: 0.2em;
}

select {
    display: block;
    background-color: white;
    border: none;
    border-radius: 10px;
    padding: 0.5em;
    font-weight: bold;
    width: 100%;
    color: black;
    font-weight: bold;
    cursor: pointer;
}

select:hover {
    box-shadow: 0 0 2px black;
}
</style>