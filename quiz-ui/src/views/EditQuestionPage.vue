<template>
     <AdminTabNav />
     <QuestionCRUForm 
     :titre="titre"
        :intitule="intitule"
        :position="position"
        :image="image"
        :possibleAnswers="possibleAnswers"
        titreForm="Editer une question"
        submitButtonText="Editer"
        @reset-question= "handleResetQuestionEvent"
        @submit-question="handleSubmitQuestionEvent"
    />
  </template>
  
  <script>
  import quizApiService from "@/services/QuizApiService";
  import AdminTabNav from "@/components/AdminTabNav.vue";
  import QuestionCRUForm from "@/components/QuestionCRUForm.vue";
  import participationStorageService from "@/services/ParticipationStorageService.js";


  export default {
    name: "EditQuestionPage",
    components: {
        AdminTabNav,
        QuestionCRUForm
    },
    data() {
      return {
        id:0,
        titre: "",
            intitule: "",
            position: 1,
            image: "",
            possibleAnswers: [],
            token: "",
            error: ""
      };
    },
    async created() {
        this.token = participationStorageService.getToken();

        if (!this.token) {
            this.$router.push("/");
            return;
        }
        this.id = this.$route.params.id;

        quizApiService.getQuestionById(this.id).then((response) => {
                if (response.status !== 200) {
                    const ERROR = `CODE : ${response.status} postQuestion`
                    return Promise.reject(ERROR);
                }
        
                this.titre = response.data.title;
                this.intitule = response.data.text;
                this.position = response.data.position;
                this.image = response.data.image;
                this.possibleAnswers = response.data.possibleAnswers;
                console.log(this.titre);

              
                
            }).catch((error) => {
                console.error(error);
                if (error.status === 401) {
                    participationStorageService.saveToken("");
                    this.$router.push("/login");
                }
            })
    },
    methods: {
        async handleSubmitQuestionEvent(form) {
            quizApiService.putQuestion(
                this.id,
                form.titre,
                form.intitule,
                form.image,
                form.position,
                form.possibleAnswers,
                this.token
            ).then((response) => {
                if (response.status !== 200) {
                    const ERROR = `CODE : ${response.status} putQuestion`
                    return Promise.reject(ERROR);
                }

                this.$router.push("/list-questions");
            }).catch((error) => {
                console.error(error);
                if (error.status === 401) {
                    participationStorageService.saveToken("");
                    this.$router.push("/login");
                }
            })
        },
        handleResetQuestionEvent(){
            this.$router.push("/list-questions");
        }
    }
  };
  </script>