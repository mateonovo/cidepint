<template>
  <section>
    <div class="container my-5">
      <h1 class="display-4 text-center">Bienvenido a CIDEPINT - Sitio público</h1>
      <hr>
      <div class="image-container">
        <img src="/public/cidepint1.jpg">
        <img src="/public/cidepint2.jpg">
        <img src="/public/cidepint3.jpg">
        <img src="/public/cidepint4.jpg">
      </div>
      <br>
      <p class="lead text-center">
        Aquí encontrarás una amplia gama de servicios ofrecidos por diversas instituciones.
        Puedes explorar y solicitar los servicios que necesitas de manera fácil y rápida.
      </p>
      <hr>
      <ul class="list-group">
        <li class="list-group-item">
            <div>
                <h2 class="h4">Búsqueda de Servicios</h2>
                <p>Realiza búsquedas eficientes para encontrar los servicios que necesitas.</p>
            </div>
        </li>
        <li class="list-group-item">
            <div>
                <h2 class="h4">Informacion de los Servicios</h2>
                <p>Observa la información del servicio e institución que estés buscando.</p>
            </div>       
        </li>
        <li class="list-group-item">
            <div>
                <h2 class="h4">Solicitud de Servicio</h2>
                <p>Inicia fácilmente una solicitud de servicio.</p>
            </div>
        </li>
      </ul>
      <br>
    </div>
  </section>
  <footer class="bg-light text-dark">
      <div class="container py-3">
            <div class="row">
                <div class="col-md-12 text-center">
                  <img id="logo" src="/public/logo.jpg" alt="Banner CIDEPINT" style="max-width: 100%; height: auto; display: inline-block;">
                </div>
            </div>
        </div>
    </footer>
</template>

<script>
export default {
  name: 'Home'
}
</script>

<style scoped>
    .image-container {
      display: grid;
      grid-template-columns: repeat(2, 1fr); 
      gap: 10px; 
      max-width: 600px; 
      margin: 0 auto; 
    }

    .image-container img {
      width: 100%; 
      height: auto;
      max-width: 100%; 
      display: block; 
    }
    hr {
      border: 1px solid #131111; 
      margin-top: 10px;
      margin-bottom: 30px; 
    }
    #logo {
    max-width: 118%;
    max-height: 118%;
    padding: 8px;
  }
</style>