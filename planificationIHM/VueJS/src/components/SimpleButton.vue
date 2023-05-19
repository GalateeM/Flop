<template>
    <input type="button" :value="value" :style="{ backgroundColor: color, fontSize: size }">
</template>

<script>
export default {
    name: 'SimpleButton',
    props: {
        value: String,
        color: String,
        size: String
    }
}
</script>

<style scoped>
input {
    border: none;
    border-radius: 10px;
    padding: 0.5em;
    margin: 10px;
    font-weight: bold;
    width: 10em;
    cursor: pointer;
    color: white;
}

input:hover {
    box-shadow: 0 0 2px black;
}
</style>