import axios from "axios";

const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}`,
  json: true,
});

export default {
  async call(method, resource, data = null, token = null) {
    var headers = {
      "Content-Type": "application/json",
    };
    if (token != null) {
      headers.authorization = "Bearer " + token;
    }

    return instance({
      method,
      headers: headers,
      url: resource,
      data,
    })
      .then((response) => {
        return { status: response.status, data: response.data };
      })
      .catch((error) => {
        console.error(error);
        return Promise.reject({
          status: error.response.status,
          error: error.response.statusText,
        });
      });
  },
  getQuizInfo() {
    return this.call("get", "quiz-info");
  },
  getQuestionById(id) {
    return this.call("get", `questions/${id}`);
  },
  getQuestionByPosition(position) {
    return this.call("get", `questions?position=${position}`);
  },
  postParticipation(playerName, answers) {
    return this.call("post", `participations`, { playerName, answers });
  },
  postLogin(myPassword) {
    return this.call("post", "login", { password: myPassword });
  },
  postQuestion(titre, intitule, image, position, possibleAnswers, token) {
    return this.call(
      "post",
      `questions`,
      {
        title: titre,
        text: intitule,
        image: image,
        position: position,
        possibleAnswers: possibleAnswers,
      },
      token
    );
  },
  getAllQuestions() {
    return this.call("get", "questions/all");
  },
  deleteQuestionById(id, token) {
    return this.call("delete", `questions/${id}`, null, token);
  },
};
