<template>
    <div class="container my-5">
      <h2 class="display-4 text-center">Solicitudes por Estado</h2>
      <hr>
      <p class="lead text-center">
        Este gráfico representa la cantidad de solicitudes que se encuentran en cada uno de los cinco estados posibles.
      </p>
      <div>
          <Pie v-if="loaded" :data="chartData" :options="chartOptions" />
      </div>
    </div>
  </template>
  
  <script>
  import { apiService } from '@/api';
  import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
  import { Pie } from 'vue-chartjs'

ChartJS.register(ArcElement, Tooltip, Legend)
  
  export default {
    components: {
        Pie
    },
    data() {
      return {
        loaded: false, 
        chartData: {
          labels: [],
          datasets: [
            {
                backgroundColor: ['#41B883', '#E46651', 'yellow', 'blue', 'orange'],
                data: []
            },
          ],
        },
        chartOptions: {
          responsive: true,
          maintainAspectRatio: false,
        },
      };
    },
    created() {
      this.fetchData();
    },
    methods: {
      async fetchData() {
        this.loaded = false
        try {
          const csrfToken = localStorage.getItem('csrfToken');
          const jwtToken = localStorage.getItem('jwt');
          if (localStorage.getItem('jwt') == null) {
            alert("Debe iniciar sesión para ver sus solicitudes");
            throw new Error("Debe iniciar sesión para ver sus solicitudes");
          }
          const respuesta = await apiService.get('api/solicitudes_por_estado', {
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${jwtToken}`,
              'X-CSRF-TOKEN': csrfToken,
            },
          });
          this.chartData.labels = respuesta.data.data.map(item => item[0]);
          this.chartData.datasets[0].data = respuesta.data.data.map(item => item[1]);
          this.loaded = true
          console.log(this.chartData.labels);
          console.log(this.chartData.datasets[0].data);
        } catch (error) {
          console.error('Error al obtener las estadísticas de solicitudes por estado', error);
          this.$router.push({ name: 'loginView' });
        }
      },
    },
  };
  </script>
  