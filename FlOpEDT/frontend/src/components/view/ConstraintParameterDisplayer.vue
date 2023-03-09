<template>
    <template v-if="idList.length == 0">
        <p>Tous</p>
    </template>
    <template v-else>
        <template v-for="itemId in idList" :key="itemId">
            <p>{{ values.get(itemId) }}</p>
        </template>
    </template>
</template>

<script setup lang="ts">
/**
 * Display a list of indexed items based on their values in a map
 * 
 * If the list of indexed items is empty, display the "all" word
 */

/**
 * Properties declaration interface of the component
 */
interface Props {
    /**
     * Id list of values to display
     */
    idList: Array<unknown>

    /**
     * Map of values to display
     */
    values: Map<unknown, unknown>
}
/**
 * Properties list of the component
 */
const props = withDefaults(defineProps<Props>(), {})

</script>

<style scoped></style>
