<template>
  <div class="container-fluid mb-4 my-5">
    <h2 class="display-4 text-center">Mis Solicitudes</h2>
    <hr>
    <div class="form-group">
      <label for="estado">Filtrar por Estado:</label>
      <select class="form-control" v-model="estado">
        <option value="">Seleccione un estado</option>
        <option value="EN PROCESO">EN PROCESO</option>
        <option value="ACEPTADA">ACEPTADA</option>
        <option value="FINALIZADA">FINALIZADA</option>
        <option value="CANCELADA">CANCELADA</option>
        <option value="RECHAZADA">RECHAZADA</option>
      </select>
    </div>


    <div class="form-group">
      <label for="fechaInicio">Fecha Inicio:</label>
      <input type="date" class="form-control" v-model="fechaInicio">
    </div>

    <div class="form-group">
      <label for="fechaFin">Fecha Fin:</label>
      <input type="date" class="form-control" v-model="fechaFin">
    </div>

    <div class="form-group">
      <button class="btn btn-primary" @click="traerSolicitud">Buscar</button>
      <button v-if="busqueda" class="btn btn-secondary" @click="deshacerBusqueda">Deshacer Búsqueda</button>
    </div>

    <div class="btn-group" style="margin-bottom: 1%;">
      <button class="btn btn-secondary" @click="ordenarPor('fecha_creacion', 'asc')">Ordenar por Fecha Ascendente</button>
      <button class="btn btn-secondary" @click="ordenarPor('fecha_creacion', 'desc')">Ordenar por Fecha Descendente</button>
      <button class="btn btn-secondary" @click="ordenarPor('estado', 'asc')">Ordenar por Estado Alfabéticamente</button>
    </div>

    <div class="table-responsive">
      <table class="table table-striped table-hover">
        <thead>
          <tr>
            <th @click="ordenarPor('nombre')">Título del Servicio</th>
            <th>Descripción</th>
            <th>Estado</th>
            <th>Fecha de Creación</th>
            <th>Fecha de Cambio de Estado</th>
            <th>Ultimo Comentario</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="solicitud in solicitudes" :key="solicitud.id">
            <td>{{ solicitud.servicio ? solicitud.servicio.nombre : 'Sin servicio' }}</td>
            <td>{{ solicitud.detalles }}</td>
            <td>{{ solicitud.estado }}</td>
            <td>{{ formatoFecha(solicitud.fecha_creacion) }}</td>
            <td>{{ formatoFecha(solicitud.fecha_cambio_estado) }}</td>
            <td>{{ solicitud.observacion_cambio_estado }}</td>
            <td>
              <button class="btn btn-primary" @click="mostrarCampoComentario(solicitud)">Comentar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <p v-if="busqueda && solicitudes && solicitudes.length == 0"> <b>No se encontraron solicitudes</b></p>

    <div v-if="solicitudConComentario">
      <div class="comentario-container">
        <label for="SolicitudComentario" class="comentario-label">
          Comentario para {{ solicitudConComentario.servicio.nombre }} (Creada el {{ formatoFecha(solicitudConComentario.fecha_creacion) }})
        </label>
        <div class="form-group">
          <input v-model="solicitudConComentario.nuevoComentario" placeholder="Ingrese su comentario" class="form-control">
          <button class="btn btn-success" @click="comentarSolicitud(solicitudConComentario)">Enviar</button>
        </div>
      </div>
    </div>

    <!-- Mostrar mensaje de éxito -->
      <div v-if="comentarioEnviado" class="alert alert-success mt-4">
        Comentario añadido con éxito a la solicitud  
      </div>

    <nav aria-label="Page navigation">
      <ul class="pagination">
        <li class="page-item" v-if="currentPage > 1">
          <a class="page-link" @click="cambiarPagina(currentPage - 1)" aria-label="Previous">
            <span aria-hidden="true">&laquo;</span>
          </a>
        </li>
        <li class="page-item" v-for="pageNumber in pages" :key="pageNumber" :class="{ 'active': currentPage == pageNumber }">
          <a class="page-link" @click="cambiarPagina(pageNumber)">{{ pageNumber }}</a>
        </li>
        <li class="page-item" v-if="currentPage < pages">
          <a class="page-link" @click="cambiarPagina(currentPage + 1)" aria-label="Next">
            <span aria-hidden="true">&raquo;</span>
          </a>
        </li>
      </ul>
    </nav>
    

  </div>
</template>

<script>
import { apiService } from '@/api';

export default {
  data() {
    return {
      estado: '',
      fechaInicio: '',
      fechaFin: '',
      busqueda: false,
      solicitudes: [],
      currentPage: 1, // Agregamos una propiedad para rastrear la página actual
      pages: 0,
      sort: '', // Agregamos una propiedad para rastrear la columna de ordenamiento
      order: '', // Agregamos una propiedad para rastrear el orden (ascendente o descendente)
      solicitudConComentario: null,
      comentarioEnviado: false
    };
  },
  methods: {

    async traerSolicitud() {
      const params = {
        page: this.currentPage,
        per_page: '3',
        sort: this.sort,
        order: this.order,
        fecha_inicio: this.fechaInicio,
        fecha_fin: this.fechaFin,
        estado: this.estado
      }
      try {
        const csrfToken = localStorage.getItem('csrfToken'); 
        const jwtToken = localStorage.getItem('jwt');
        if(localStorage.getItem('jwt') == null){
            alert("Debe iniciar sesión para ver sus solicitudes");
            throw new Error("Debe iniciar sesión para ver sus solicitudes");
        }
        const respuesta = await apiService.get('api/me/requests', { params
        }, 
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${jwtToken}`,
            'X-CSRF-TOKEN': csrfToken,
          },
        });
        this.solicitudes = respuesta.data.data;
        this.comentarioEnviado = false
        this.pages = respuesta.data.pages
        this.busqueda = true;
      } catch (error) {
        console.error('Error al obtener o filtrar las solicitudes', error);
        this.$router.push({ name: 'loginView' });
      }},

    deshacerBusqueda() {
      this.busqueda = false;
      this.estado = '';
      this.fechaInicio = '';
      this.fechaFin = '';
      this.sort = ''; // Reiniciar la columna de ordenamiento
      this.order = ''; // Reiniciar el orden (ascendente por defecto)
      this.solicitudes = [];
      this.comentarioEnviado = false

    },

    ordenarPor(sort, order) {
      this.order = order;
      this.sort = sort;
    },

    cambiarPagina(pageNumber) {
      this.currentPage = pageNumber;
      this.traerSolicitud();
    },

    formatoFecha(fecha) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(fecha).toLocaleDateString('es-ES', options);
    },


    mostrarCampoComentario(solicitud) {
      // Asignar la solicitud actual a la propiedad solicitudConComentario
      this.solicitudConComentario = solicitud;
    },

    async comentarSolicitud(solicitud) {
      try {
        const comentario = solicitud.nuevoComentario
        const csrfToken = localStorage.getItem('csrfToken'); 
        const jwtToken = localStorage.getItem('jwt');
        if(localStorage.getItem('jwt') == null){
            alert("Debe iniciar sesión para comentar una solicitud");
            throw new Error("Debe iniciar sesión para comentar una solicitud");
        }
        const respuesta = await apiService.post(`api/me/requests/${solicitud.id}/notes`, { comentario
        }, 
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${jwtToken}`,
            'X-CSRF-TOKEN': csrfToken,
          },
        });
        
        // Limpiar el campo de comentario después de enviar el comentario
        this.comentarioEnviado = true
        solicitud.nuevoComentario = '';
        this.solicitudConComentario = null
      } catch (error) {
        console.error('Error al comentar una solicitud', error);
        this.$router.push({ name: 'loginView' });
      }
    },

  },}
</script>

<style>
 .form-group {
    display: flex;
    justify-content: space-between;
  }
</style>
