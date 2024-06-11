import { apiService } from '@/api';
import axios from 'axios';

export default {
  props: ['id'],
  data() {
    return {
      servicio: {},
      institucion: {},
    };
  },
  mounted() {
    this.obtenerServicio();
  
  },
  methods: {
    async obtenerServicio() {
      try {
        const respuesta = await apiService.get(`/api/services/${this.id}`);
        this.servicio = respuesta.data;
        this.obtenerInstitucion(this.servicio.institucion_id);
      } catch (error) {
        console.error('Error al obtener la información del servicio', error);
      }
    },
    async obtenerInstitucion(institucionId) {
      try {
        const respuesta = await apiService.get(`/api/instituciones/${institucionId}`);
        this.institucion = respuesta.data;
        this.infoMapa(this.institucion.calle, this.institucion.numero, this.institucion.contacto, this.institucion.web)
      } catch (error) {
        console.error('Error al obtener la información de la institución', error);
      }
    },
    async infoMapa(calle, nro, contacto, web) {
      try {
        const info = await axios.get(`https://nominatim.openstreetmap.org/search?country=argentina&city=la+plata&street=${nro}+Calle+${calle}&format=json`)
        const map = L.map('mapa').setView([-34.91895294495346, -57.95574638183875], 14);
        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);
        const marker = L.marker([info.data[0].lat, info.data[0].lon]).addTo(map);
        marker.bindPopup("Telefono: " + contacto + "<br>Web: " + web).openPopup();
      } catch(error) {
          console.error('Error al obtener la información de geocoding', error);
      }

    },
  },

};