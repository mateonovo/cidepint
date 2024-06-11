<template>
<div class="container my-5">
    <h2 class="display-4 text-center">Top 10 instituciones con mejor tiempo de resolución.</h2>
    <hr>
    <p class="lead text-center">
    El tiempo de resolución representa el período desde la creación de la solicitud hasta su finalización.
    </p>
    <ul class="list-group">
        <li
            v-for="(institucion, index) in instituciones"
            :key="institucion.id"
            class="list-group-item d-flex justify-content-between align-items-center"
        >
        <span class="badge bg-primary rounded-pill">{{ index + 1 }}</span>
        {{ institucion.nombre }}
    </li>
    </ul>
</div>
</template>

<script>
import { apiService } from "../api";

export default {
data() {
    return {
    instituciones: [],
    };
},
created() {
    this.obtenerInstituciones();
},
methods: {
    async obtenerInstituciones() {
    try {
        const respuesta = await apiService.get('/api/top-institutions');
        this.instituciones = respuesta.data.data;
    } catch (error) {
        console.log('Error al obtener la información de las instituciones', error);
    }
    },
},
};
</script>
  