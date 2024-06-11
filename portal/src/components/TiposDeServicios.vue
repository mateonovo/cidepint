<template>
    <div class="form-group">
      <label for="seleccionTipoServicio">Tipo de Servicio:</label>
      <select id="seleccionTipoServicio" class="form-control" v-model="tipoServicio" @change="emitTipoServicio">
        <option value="">Todos</option>
        <option v-for="tipo in tiposDeServicios" :key="tipo">
          {{ tipo }}
        </option>
      </select>
    </div>
</template>
  
<script>
  import { apiService } from '@/api';
  
  export default {
    props: ['tipoElegido'],

    data() {
      return {
        tipoServicio: this.tipoElegido,
        tiposDeServicios: [],
      };
    },

    async created() {
      await this.obtenerTiposDeServicio();
    },

    methods: {
      async obtenerTiposDeServicio() {
        try {
          const respuesta = await apiService.get('/api/services-type');
          this.tiposDeServicios = respuesta.data.data;
        } catch (error) {
          console.error('Error al obtener tipos de servicio:', error);
        }
      },
      emitTipoServicio() {
        this.$emit('tipo-servicio-seleccionado', this.tipoServicio);
      }
    },
    watch: {
      tipoElegido: function (nuevoValor) {
        this.tipoServicio = nuevoValor;
      },
      tipoServicio: function (nuevoValor) {
        this.$emit('update:tipoElegido', nuevoValor);
      },
    }
  };
</script>

<style>
</style>
  