<template>
    <template v-for="item in values" :key="item">
        <span>{{ item + " "}}</span>
    </template>
</template>

<script setup lang="ts">
/**
 * Display each items of a list
 */

/**
 * Properties declaration interface of the component
 */
interface Props {
    /**
     * List of items
     */
    values: Array<unknown>
}
/**
 * Properties list of the component
 */
const props = withDefaults(defineProps<Props>(), {})

</script>

<style scoped></style>
