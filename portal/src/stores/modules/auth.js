// auth.js
import { defineStore } from 'pinia';
import { apiService } from '@/api';

export const useAuthStore = defineStore({
  id: 'auth',
  state: () => ({
    user: null,
    isLoggedIn:false
  }),
  getters: {
    getUser: (state) => state.user,
    getIsLoggedIn: (state) => state.isLoggedIn,
    getUserPermissions: (state) => state.user ? state.user.statistics_permissions : []
  },
  persist: {
    storage: sessionStorage,
    paths: ['isLoggedIn', 'user'],
  },
  actions: {
    async axiosUser() {
      try {

        const userResponse = await apiService.get('api/user_jwt', {
          headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('jwt')}`
         }        
          });
        console.log(userResponse.data,"EN AUTH");
        this.setUser(userResponse.data);
      } catch (error) {
        console.error(error);
        this.error = true;
      }},
  async logout() {  
        try {
           const response = await apiService.get('api/logout_jwt',{
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('jwt')}`
            }})
           localStorage.removeItem('jwt');
           console.log(response.data.message);
           this.logoutUser()
      }
      catch (error) {
          console.error(error);
        }},

    setUser(user) {
      this.user = user;
      this.isLoggedIn = true;
    },
    logoutUser() {
      this.user = null;
      this.isLoggedIn = false;
    },
  },
});
