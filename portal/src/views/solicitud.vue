<template>
  <br>
  <br>
    <div class="container">
      <h3 class="display-4">Usted va a solicitar {{ servicio.nombre }}, de la institución {{ institucion.nombre }} </h3>
      <br>
      <h4 class="mt-4">Por favor, complete este campo indicando detalles de su solicitud</h4>
      <form @submit.prevent="enviarSolicitud" class="mt-4">
        <div class="form-group">
          <textarea id="detalle" v-model="detalle" class="form-control" required></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Enviar Solicitud</button>
      </form>
      <button @click="volverAtras" class="btn btn-secondary mt-4">Volver atrás</button> 
      <div v-if="solicitudEnviada" class="alert alert-success mt-4">
        Solicitud enviada con éxito al servicio : "{{ this.servicio.nombre}}"  
      </div>
    </div>
  </template>
  
<script>
import { apiService } from '@/api';


  export default {
    name: 'Solicitud',
    data() {
      return {
        detalle: "",
        solicitudEnviada: false,
        servicio : {},
        institucion : {},
      };
    },
    created() {
        this.obtenerServicio();
        this.obtenerInstitucion(this.$route.params.institucion_id);
  },
    methods: {
      volverAtras() {
        window.history.back();
    },
      async enviarSolicitud() {
  try {
    const csrfToken = localStorage.getItem('csrfToken'); 
    const jwtToken = localStorage.getItem('jwt');
    if (!this.institucion.habilitado){
        alert("El centro no está habilitado");
        throw new Error("Este centro no está habilitado");
    }
    if(!this.servicio.habilitado){
        alert("El servicio no está habilitado");
        throw new Error("Este servicio no está habilitado");
    }
    if(localStorage.getItem('jwt') == null){
        alert("Debe iniciar sesión para enviar una solicitud");
        this.$router.push({ name: 'loginView' });
    }
    const respuesta = await apiService.post('api/me/requests', {
      detalles: this.detalle,
      servicio_id: this.$route.params.id,
    }, 
    {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${jwtToken}`,
        'X-CSRF-TOKEN': csrfToken,
      },
    });

    console.log(respuesta.data);
    this.solicitudEnviada = true;
  } catch (error) {
    console.error('Error al enviar la solicitud', error);
  }},

  async obtenerServicio() {
      try {
        const respuesta = await apiService.get(`/api/services/${this.$route.params.id}`);
        this.servicio = respuesta.data;
      } catch (error) {
        console.error('Error al obtener la información del servicio', error);
      }
    },
 async obtenerInstitucion(institucionId) {
      try {
        const respuesta = await apiService.get(`/api/instituciones/${institucionId}`);
        this.institucion = respuesta.data;
      } catch (error) {
        console.error('Error al obtener la información de la institución', error);
      }
    },
    },
  };
</script>

  