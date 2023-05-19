<template>
    <div>
        <label for="select">{{ label }}</label>
        <select name="select" @change="$emit('value', $event.target.value)">
            <option :selected="$parent.edit == -1"></option>
            <option v-for="option in options" :key="option.id" :value="option.id"
                :selected="$parent.edit != -1 && option.id == $parent.savedCourses[$parent.edit][edit]">{{ option.name }}</option>
        </select>
    </div>
</template>

<script>
export default {
    name: 'SimpleInput',
    props: ['label', 'options', 'edit'],
    emits: ['value']
}
</script>

<style scoped>
div {
    width: 15rem;
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