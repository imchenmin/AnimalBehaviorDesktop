<template lang="">

</template>
<script lang="ts">
import useStore from '../store'
export default {
  setup() {
    const { version, experiments } = useStore();
    experiments.loadProject()
    return {
      version
    }
  }
}
</script>
<style>
.intro-panel {
  width: 600px;
  margin: auto;
  margin-top: 50px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>