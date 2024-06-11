<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div v-if="!loggedIn" class="card">
          <div class="card-body d-flex flex-column align-items-center">
            <img src="/public/logo_login.png" style="max-width: 125px;" class="mb-3">
            <h2 class="card-title text-center">Iniciar sesión</h2>
            <form @submit.prevent="login" class="w-100">
              <div class="mb-3">
                <label for="email" class="form-label">Correo electrónico:</label>
                <input v-model="user.email" type="email" id="email" class="form-control" required>
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Contraseña:</label>
                <input v-model="user.password" type="password" id="password" class="form-control" required>
              </div>
              <button type="submit" class="btn btn-primary btn-block">Iniciar sesión</button>
              <p v-if="error" class="text-danger text-center mt-2">Correo electrónico o contraseña incorrectos</p>
            </form>
        </div>

          <br>
            <p class="text-inverse text-center">
              ¿No tenes una cuenta? <a :href="registerURL" data-abc="true">Registrate</a>
            </p>
      </div>
    </div>
  </div>
  </div>
  <p v-if="success" class="success-message">Inicio de sesión exitoso!</p>
</template>

<script>

import { apiService } from '@/api';
import { baseURL } from '@/api';
import { useAuthStore } from '@/stores/modules/auth';

export default {
  data() {
    return {
      user: {
        email: '',
        password: ''
      },
      error: false,
      success: false
    };
  },
  created() {
    this.store = useAuthStore();
  },
  computed: {
    loggedIn() {
      return this.store.isLoggedIn;
    },
    registerURL() {
      return `${baseURL}/sesion/register`;
    }
  },
  methods: {
    async login() {
      try {
        const userData = {
          email: this.user.email,
          password: this.user.password
        };

        const response = await apiService.post('api/login_jwt', userData, {
          headers: {
            'Content-Type': 'application/json'
          }
        });
        console.log('login : ',response.status , response.statusText);
        localStorage.setItem('jwt', response.data.token);
        this.success = true;
        await this.store.axiosUser();
        this.$router.push({ name: 'Home' });

      } catch (error) {
        console.error(error);
        this.error = true;
      }
    }
  }
};
</script>

<style scoped>

.login-form {
  max-width: 400px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f5f5f5;
}

.success-message {
  color: green;
  font-weight: bold;
  margin-top: 10px;
  text-align: center
}
</style>
