<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <router-link to="/" class="navbar-brand">CIDEPINT</router-link>

    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav mr-auto">
        <li class="nav-item">
          <router-link to="/servicios" class="nav-link">Servicios</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/contacto" class="nav-link">Contacto</router-link>
        </li>
        <li v-if="loggedIn" class="nav-item">
          <router-link to="/solicitudes" class="nav-link">Mis Solicitudes</router-link>
        </li>
        <li v-if="tienePermisosDeEstadistica" class="nav-item">
          <router-link to="/estadisticas" class="nav-link">Estadísticas</router-link>
        </li>
      </ul>

      <ul class="navbar-nav ml-auto">
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownProfile" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            <font-awesome-icon icon="fa-solid fa-circle-user" />
          </a>

          <div class="dropdown-menu dropdown-menu-right" aria-labelledby="navbarDropdownProfile">
            <router-link v-if="!loggedIn" to="/login" class="dropdown-item">Iniciar sesión</router-link>
            <a v-else href="#" class="dropdown-item" @click.prevent="logout">Cerrar sesión</a>
          </div>
        </li>
      </ul>
    </div>
  </nav>
</template>

  
<script>
  import { useAuthStore } from '@/stores/modules/auth';
  import logout from '../components/logout.vue'



  export default {
    name: 'Navbar',

    components: {
      logout
  },
  created() {
    this.store = useAuthStore();
  },
  
  computed: {
    loggedIn(){
      return this.store.getIsLoggedIn;
    },

    tienePermisosDeEstadistica() {
      const userPermissions = this.store.getUserPermissions;
      if (userPermissions) {
        return userPermissions.includes('statistics_index');
      } else {
        return false;
      }
    }
  },
  methods: {
  async logout() {
      try {
        await this.store.logout();
        this.$router.push({ name: 'Home' });
      } catch (error) {
        this.$router.push({ name: 'loginView' });
        console.error(error);
      }
    }
  }
  }
  </script>
  
  <style scoped>
  nav {
    background-color: #333;
    width: 100%;
    position: fixed; 
    top: 0;
    left: 0;
    z-index: 1000; 
  } 
  ul {
    list-style-type: none;
    padding: 0;
  }
  li {
    display: inline-block;
    margin: 0 10px;
  }
  a {
    text-decoration: none;
  }

</style>