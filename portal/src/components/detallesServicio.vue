<template>
  <br>
  <br>
  <div class="row">
    <div class="col-sm-6">
      <div class="card">
        <div class="card-body">
          <h1> Servicio </h1>
          <p class="card-title"><b>Nombre: </b>{{servicio.nombre}}</p>
          <p class="card-text"><b>Descripcion: </b>{{ servicio.descripcion }}</p>
          <p class="card-text"><b>Tipo: </b>{{ servicio.tipo_servicio }}</p>
          <p class="card-text"><b>Palabras Clave: </b>{{ servicio.keywords}}</p>
          <p class="card-text" v-if="servicio.habilitado"><b>Habilitado: </b>Si</p>
          <p class="card-text" v-else><b>Habilitado: </b>No</p>
          <router-link :to="{ name: 'solicitud', params: { id: servicio.id, institucion_id: `${institucion.id}` } }">
                <button class="btn btn-primary">Solicitar</button>
          </router-link>
        </div>
      </div>
    </div>
    <div class="col-sm-6">
      <div class="card">
        <div class="card-body">
        <h1> Institucion </h1>
        <p class="card-title"><b>Nombre: </b>{{institucion.nombre}}</p>
        <p class="card-text"><b>Informacion: </b>{{ institucion.informacion }}</p>
        <p class="card-text"><b>Calle: </b>{{ institucion.calle }}</p>
        <p class="card-text"><b>Numero: </b>{{ institucion.numero }}</p>
        <p class="card-text"><b>Horarios: </b>{{ institucion.horarios }}</p>
        <p class="card-text" v-if="institucion.habilitado"><b>Habilitado: </b>Si</p>
        <p class="card-text" v-else><b>Habilitado: </b>No</p>
        <p class="card-text"></p>
       </div>
     </div>
   </div>
  </div>
  <br>
  <br>
  <hr>
    <br>
    <div class="row mt-4">
      <div class="col">
        <div id="mapa" style="height: 400px;"></div>
      </div>
    </div>
</template>



<script>
import detalleServicio from './javascript/detalleServicio.js';

export default detalleServicio;
</script>

<style>
#mapa { 
    height: 400px;
    display: block;
    margin-left: auto;
    margin-right: auto;
    width: 1000px
}
</style>
