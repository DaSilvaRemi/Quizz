import axios from "axios";

const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}`,
  json: true,
});

export default {
  /**
   * Makes an HTTP request to the API.
   * @param {string} method - The HTTP method (e.g., "get", "post", "put", "delete").
   * @param {string} resource - The API resource endpoint.
   * @param {Object} data - The data to be sent in the request body.
   * @param {string} token - The token for authentication.
   * @returns {Promise} A Promise that resolves to the response from the API.
  */
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
  /**
   * Retrieves the quiz information from the API.
   * @returns {Promise} A Promise that resolves to the quiz information.
   */
  getQuizInfo() {
    return this.call("get", "quiz-info");
  },
  /**
   * Retrieves a question by its ID from the API.
   * @param {number} id - The ID of the question.
   * @returns {Promise} A Promise that resolves to the question data.
   */
  getQuestionById(id) {
    return this.call("get", `questions/${id}`);
  },
  /**
   * Retrieves a question by its position from the API.
   * @param {number} position - The position of the question.
   * @returns {Promise} A Promise that resolves to the question data.
   */
  getQuestionByPosition(position) {
    return this.call("get", `questions?position=${position}`);
  },
  /**
   * Posts the participation data to the API.
   * @param {string} playerName - The name of the player.
   * @param {Array} answers - The player's answers.
   * @returns {Promise} A Promise that resolves to the response from the API.
   */
  postParticipation(playerName, answers) {
    return this.call("post", `participations`, { playerName, answers });
  },
  /**
   * Posts the login data to the API for authentication.
   * @param {string} myPassword - The password for authentication.
   * @returns {Promise} A Promise that resolves to the response from the API.
   */
  postLogin(myPassword) {
    return this.call("post", "login", { password: myPassword });
  },
  /**
   * Posts a new question to the API.
   * @param {string} titre - The title of the question.
   * @param {string} intitule - The text of the question.
   * @param {string} image - The URL of the question image.
   * @param {number} position - The position of the question.
   * @param {Array} possibleAnswers - The possible answers for the question.
   * @param {string} token - The token for authentication.
   * @returns {Promise} A Promise that resolves to the response from the API.
   */
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
  /**
   * Updates an existing question in the API.
   * @param {number} id - The ID of the question.
   * @param {string} titre - The updated title of the question.
   * @param {string} intitule - The updated text of the question.
   * @param {string} image - The updated URL of the question image.
   * @param {number} position - The updated position of the question.
   * @param {Array} possibleAnswers - The updated possible answers for the question.
   * @param {string} token - The token for authentication.
   * @returns {Promise} A Promise that resolves to the response from the API.
   */
  putQuestion(id, titre, intitule, image, position, possibleAnswers, token) {
    return this.call(
      "put",
      `questions/${id}`,
      {
        id: id,
        title: titre,
        text: intitule,
        image: image,
        position: position,
        possibleAnswers: possibleAnswers,
      },
      token
    );
  },
  /**
   * Retrieves all questions from the API.
   * @returns {Promise} A Promise that resolves to all the questions.
   */
  getAllQuestions() {
    return this.call("get", "questions/all");
  },
  /**
   * Deletes a question by its ID from the API.
   * @param {number} id - The ID of the question to be deleted.
   * @param {string} token - The token for authentication.
   * @returns {Promise} A Promise that resolves to the response from the API.
   */
  deleteQuestionById(id, token) {
    return this.call("delete", `questions/${id}`, null, token);
  },
};
