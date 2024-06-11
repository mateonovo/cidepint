<template>
<div class="container my-5">
    <h2 class="display-4 text-center">Información de Contacto</h2>
    <hr>
    <div class="row mt-4">
        <div class="col-md-4">
            <div class="card">
                <div class="card-body text-center">
                    <font-awesome-icon icon="fas fa-envelope fa-3x mb-3"/>
                    <h5 class="card-title">Email</h5>
                    <p class="card-text">{{ contacto.email }}</p>
                </div>
            </div>
        </div>

        <div class="col-md-4">
            <div class="card">
                <div class="card-body text-center">
                    <font-awesome-icon icon="fas fa-phone fa-3x mb-3"/>
                    <h5 class="card-title">Teléfono</h5>
                    <p class="card-text">{{ contacto.telefono }}</p>
                </div>
            </div>
        </div>

        <div class="col-md-4">
            <div class="card">
                <div class="card-body text-center">
                  <font-awesome-icon icon="fa-solid fa-house"/>
                    <h5 class="card-title">Dirección</h5>
                    <p class="card-text">{{ contacto.direccion }}</p>
                </div>
            </div>
        </div>
    </div>
</div>

</template>
<script>
import { apiService } from '@/api';

export default {
  data() {
    return {
      contacto: {}
    };
  },
  methods: {
    async obtenerInformacionDeContacto() {
      try {
        const respuesta = await apiService.get('api/contacto');
        this.contacto = respuesta.data;
      } catch (error) {
        console.error('Error al obtener la información de contacto', error);
      }
    }
  },
  mounted() {
    this.obtenerInformacionDeContacto();
  }
}
</script>

<style>
    hr {
      border: 1px solid #131111; 
      margin-top: 10px;
      margin-bottom: 30px; 
    }
</style>