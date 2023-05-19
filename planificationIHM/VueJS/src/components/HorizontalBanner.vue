<template>
    <div>
        <div class="banner" :style="{ backgroundColor: color }">
            {{ value }}
            <span id="buttons">
                <span id="edit" title="Éditer" @click="$emit('edit')">✎</span>
                <span id="delete" title="Supprimer" @click="$emit('delete')">✖</span>
            </span>
        </div>
    </div>
</template>

<script>
export default {
    name: 'HorizontalBanner',
    props: {
        value: String,
        color: String
    }
}
</script>

<style scoped>
#buttons {
    position: absolute;
    cursor: pointer;
    right: 3.5%;
}

.banner {
    border: none;
    border-radius: 10px;
    padding: 0.2%;
    margin-left: 2.5%;
    margin-right: 2.5%;
    margin-bottom: 5px;
    font-size: 18px;
    color: white;
    text-align: center;
    font-weight: bold;
    overflow: hidden;
}

.banner:hover {
    box-shadow: 0 0 2px black;
}

#edit {
    right: 10%;
    margin-right: 0.2em;
}

#edit:hover {
    color: orange;
}

#delete {
    right: 10%;
}

#delete:hover {
    color: #E90B0B;
}
</style>