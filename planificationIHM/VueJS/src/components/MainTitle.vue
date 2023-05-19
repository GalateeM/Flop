<template>
    <h1>{{ value }}</h1>
</template>

<script>
export default {
    name: 'MainTitle',
    props: {
        value: String
    }
}
</script>

<style scoped>
h1 {
    position: absolute;
    text-align: center;
    width: 100%;
    margin-top: 1%;
    font-size: 110%;
}
</style>