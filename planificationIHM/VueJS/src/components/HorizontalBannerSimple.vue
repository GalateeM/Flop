<template>
    <div>
        <div class="banner" :style="{ backgroundColor: color }">{{ value }}</div>
    </div>
</template>

<script>
export default {
    name: 'HorizontalBannerSimple',
    props: {
        value: String,
        color: String
    }
}
</script>

<style scoped>

.banner {
    border: none;
    border-radius: 10px;
    padding: 0.2%;
    margin-left: 2.5%;
    margin-right: 2.5%;
    margin-bottom: 5px;
    cursor: pointer;
    font-size: 18px;
    color: white;
    text-align: center;
    font-weight: bold;
}

.banner:hover {
    box-shadow: 0 0 2px black;
}
</style>