<template>
project {{current_exp.name}}
</template>
<script lang="ts" setup>
import useStore from '../store'
import { computed } from 'vue'

const props = defineProps({
  _id: String
})
const { experiments } = useStore()
console.log(props)
const current_exp = computed(() => experiments.get_from_id(props._id))
</script>
<style>

</style>