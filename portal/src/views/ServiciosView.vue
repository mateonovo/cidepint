<template>
  <div class="container-fluid mb-4 my-5">
    <h2 class="display-4 text-center">Servicios</h2>
    <hr>

    <TiposDeServicios :selectedTipo="tipoServicio" @tipo-servicio-seleccionado="actualizarTipoServicio"></TiposDeServicios>

    <div class="form-group">
      <input type="text" class="form-control" v-model="nombre" placeholder="Buscar por título">
    </div>

    <div class="form-group">
      <input type="text" class="form-control" v-model="descripcion" placeholder="Buscar por descripción">
    </div>

    <div class="form-group">
      <input type="text" class="form-control" v-model="institucion" placeholder="Buscar por institución">
    </div>

    <div class="form-group">
      <input type="text" class="form-control" v-model="keywords" placeholder="Buscar por palabras clave">
    </div>

    <div class="form-group">
      <button class="btn btn-primary" @click="buscarServicios">Buscar</button>
      <button v-if="busqueda" class="btn btn-secondary" @click="deshacerBusqueda">Deshacer Búsqueda</button>
    </div>

    <div class="table-responsive">
      <table class="table table-striped table-hover">
        <thead>
          <tr>
            <th>Título</th>
            <th>Descripción</th>
            <th>Institución</th>
            <th>Tags</th>
            <th>Tipo de Servicio</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="servicio in servicios.data" :key="servicio.id">
            <router-link :to="{name: 'detallesServicio', params: { id: servicio.id } }">
            <td>{{ servicio.nombre }}</td>
            </router-link>
            <td>{{ servicio.descripcion }}</td>
            <td>{{ servicio.institucion }}</td>
            <td>{{ servicio.keywords }}</td>
            <td>{{ servicio.tipo_servicio }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <nav aria-label="Page navigation">
      <ul class="pagination">
        <li class="page-item" v-if="servicios.page > 1">
          <a class="page-link" @click="cambiarPagina(servicios.page - 1)" aria-label="Previous">
            <span aria-hidden="true">&laquo;</span>
          </a>
        </li>
        <li class="page-item" v-for="pageNumber in servicios.pages" :key="pageNumber" :class="{ 'active': servicios.page == pageNumber }">
          <a class="page-link" @click="cambiarPagina(pageNumber)">{{ pageNumber }}</a>
        </li>
        <li class="page-item" v-if="servicios.page < servicios.pages">
          <a class="page-link" @click="cambiarPagina(servicios.page + 1)" aria-label="Next">
            <span aria-hidden="true">&raquo;</span>
          </a>
        </li>
      </ul>
    </nav>
  </div>
</template>
  
<script>
import { apiService } from '@/api';
import TiposDeServicios from '../components/TiposDeServicios.vue';

export default {
  data() {
    return {
      servicios: {
        items: [],
        page: 1,
        per_page: 3,
        total: 0,
        pages: 0
      },
      busqueda: false,
      nombre: '',
      descripcion: '',
      institucion: '',
      keywords: '',
      tipoServicio: ''
    };
  },
  components: {
    TiposDeServicios
  },
  methods: {
    async obtenerServicios() {
      try {
        const respuesta = await apiService.get('api/all_services', {
          params: {
            page: this.servicios.page,
            per_page: this.servicios.per_page
          }  
        });
        this.servicios = respuesta.data;
        this.busqueda = false;
      } catch (error) {
        console.error('Error al obtener los servicios', error);
      }
    },
    async buscarServicios() {
      try {
        if (!this.busqueda) {
          this.servicios.page = 1;
        }
        const respuesta = await apiService.get('api/search_services', {
          params: {
            nombre: this.nombre,
            descripcion: this.descripcion,
            institucion: this.institucion,
            keywords: this.keywords,
            tipo_servicio: this.tipoServicio,
            page: this.servicios.page,
            per_page: this.servicios.per_page
          }
        });
        this.servicios = respuesta.data;
        this.busqueda = true;
      } catch(error) {
          console.error('Error al obtener los servicios', error);
      }
    },
    cambiarPagina(pageNumber) {
      if (pageNumber >= 1 && pageNumber <= this.servicios.pages) {
        this.servicios.page = pageNumber;
        if(!this.busqueda) {
          this.obtenerServicios();
        } else {
          this.buscarServicios();
        }
      }
    },
    actualizarTipoServicio(valor) {
      this.tipoServicio = valor;
    },
    deshacerBusqueda() {
      console.log("DESHACER");
      this.nombre = '';
      this.descripcion = '';
      this.institucion = '';
      this.keywords = '';
      this.tipoServicio = '';
      this.busqueda = false;
      this.servicios.page = 1;
      this.obtenerServicios();

    }
  },
  mounted() {
    this.obtenerServicios();
  }
}
</script>

<style>
 .form-group {
    display: flex;
    justify-content: space-between;
  }
</style>