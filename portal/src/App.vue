<template>
  <div class="max-w-7xl mx-auto">
    
    <Navbar />
    <router-view></router-view>
    
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue'

export default {
  components: {
    Navbar
  }
}
</script>
