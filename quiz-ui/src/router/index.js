import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../views/HomePage.vue";
import NewQuizPage from "../views/NewQuizPage.vue";
import QuestionsManager from "../views/QuestionsManager.vue";
import ScorePage from "../views/ScorePage.vue";
import AdminLogin from "../views/AdminLogin.vue";
import CreateQuestionPage from "../views/CreateQuestionPage.vue";
import ListQuestionsPage from "../views/ListQuestionsPage.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomePage,
    },
    {
      path: "/new-quiz",
      name: "newQuiz",
      component: NewQuizPage,
    },
    {
      path: "/questions",
      name: "questions",
      component: QuestionsManager,
    },
    {
      path: "/score",
      name: "score",
      component: ScorePage,
    },
    {
      path: "/login",
      name: "login",
      component: AdminLogin,
    },
    {
      path: "/create-question",
      name: "createQuestion",
      component: CreateQuestionPage,
    },
    {
      path: "/list-questions",
      name: "listQuestions",
      component: ListQuestionsPage,
    },
    {
      path: "/edit-questions/:id",
      name: "editQuestion",
      component: null,
    },
  ],
});

export default router;
