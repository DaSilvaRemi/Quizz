<template>
  <header>
    <div class="wrapper">
      <nav class="navbar navbar-expand-lg bg-body-tertiary navbar-light bg-light">
        <div class="container-fluid">
          <RouterLink class="navbar-brand" to="/">Quiz</RouterLink>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              <li class="nav-item">
                <RouterLink class="nav-link active" aria-current="page" to="/">Accueil</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" to="/new-quiz">Nouveau quiz</RouterLink>
              </li>
              <li class="nav-item">
                <button class="nav-link" @click="handleClickAdmin">Admin</button>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </div>
  </header>
</template>

<script>
/**
 * Component: AppHeader
 * Description: Represents the header component of the application.
 *
 * Data:
 *   - token: The token retrieved from the participation storage service.
 *
 * Methods:
 *   - handleClickAdmin: Handles the click event on the Admin button and redirects the user to the appropriate route based on the token.
 *                        If the token is not available, it redirects to the login page. Otherwise, it redirects to the list of questions page.
 */

import { RouterLink } from 'vue-router';
import participationStorageService from "@/services/ParticipationStorageService.js";

export default {
  name: "AppHeader",
  data(){
    return {
      token: participationStorageService.getToken(),
    }
  },
  methods: {
    /**
     * Handles the click event on the Admin button and redirects the user to the appropriate route based on the token.
     * If the token is not available, it redirects to the login page. Otherwise, it redirects to the list of questions page.
     */
    handleClickAdmin() {
      const TOKEN = participationStorageService.getToken();

        if(!TOKEN){
            this.$router.push("/login");
        }else{
            this.$router.push('/list-questions');
        }
    },
  }
};
</script>