<template>
    <ConstraintManagerAdapter :showDoc="showDoc" @updateShowDoc="swap"></ConstraintManagerAdapter>
</template>

<script setup lang="ts">
import { ref} from 'vue'
import ConstraintManagerAdapter from '@/components/adapter/ConstraintManagerAdapter.vue'


const showDoc = ref(false)

/**
 * this function change the value of the showDoc
 */
function swap() {
    showDoc.value = !showDoc.value
}
</script>
