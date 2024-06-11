<script>
import { apiService } from '@/api';
import { useAuthStore } from '@/stores/modules/auth';

export default {

  created() {
    this.store = useAuthStore();
  },

  computed: {
    loggedIn() {
      return this.store.isLoggedIn;
    }
  },
  
  methods: {
    async logout() {  
      try {
         const response = await apiService.get('api/logout_jwt',{
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('jwt')}`
          }})
         localStorage.removeItem('jwt');
         console.log(response.data.message);
         this.store.logoutUser()
         this.$router.push({ name: 'Home' });
    }
    catch (error) {
        this.$router.push({ name: 'loginView' });
        console.error(error);
      }},


    }}
</script>
