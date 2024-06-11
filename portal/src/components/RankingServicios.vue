<template>
  <div class="container my-5">
    <h2 class="display-4 text-center">Solicitudes por Servicio</h2>
    <hr>
    <p class="lead text-center">
      Este gráfico representa la cantidad de solicitudes realizadas a cada servicio
    </p>
    <div>
      <Chart
        v-if="loaded"
        type="bar"
        :data="chartData"
        :options="chartOptions"
      />
    </div>
  </div>
</template>

<script>
import { apiService } from '@/api';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from 'chart.js';
import {
  Chart,
} from 'vue-chartjs';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default {
  components: {
    Chart,
  },
  data() {
    return {
      loaded: false,
      chartData: {
        labels: [],
        datasets: [
          {
            label: 'Solicitudes por Servicio',
            backgroundColor: ['blue', 'green', 'yellow', 'red', 'orange'],
            data: [],
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
      this.loaded = false;
      try {
        const csrfToken = localStorage.getItem('csrfToken');
        const jwtToken = localStorage.getItem('jwt');
        if (localStorage.getItem('jwt') == null) {
          alert("Debe iniciar sesión para ver sus solicitudes");
          throw new Error("Debe iniciar sesión para ver sus solicitudes");
        }
        const respuesta = await apiService.get('api/ranking_servicios', {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${jwtToken}`,
            'X-CSRF-TOKEN': csrfToken,
          },
        });

        
        this.chartData.labels = respuesta.data.data.map(item => item.servicio);
        this.chartData.datasets[0].data = respuesta.data.data.map(item => item.cantidad_solicitudes);
        this.loaded = true;
        console.log(respuesta.data);
        console.log(this.chartData.labels);
        console.log(this.chartData.datasets[0].data);
      } catch (error) {
        console.error('Error al obtener las estadísticas de solicitudes por servicio', error);
        this.$router.push({ name: 'loginView' });
      }
    },
  },
};
</script>
