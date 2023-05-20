export default {
    /**
     * Clears all data from the local storage.
     */
    clear() {
        window.localStorage.clear()
    },
    /**
     * Retrieves the player name from the local storage.
     * @returns {string} The player name.
     */
    getPlayerName() {
        return window.localStorage.getItem("playerName");
    },
    /**
     * Saves the player name in the local storage.
     * @param {string} playerName - The player name to be saved.
     */
    savePlayerName(playerName) {
        window.localStorage.setItem("playerName", playerName);
    },
    /**
     * Retrieves the participation score from the local storage.
     * @returns {number} The participation score.
     */
    getParticipationScore() {
        return window.localStorage.getItem("participationScore");
    },
    /**
     * Saves the participation score in the local storage.
     * @param {number} participationScore - The participation score to be saved.
     */
    saveParticipationScore(participationScore) {
        window.localStorage.setItem("participationScore", participationScore);
    },
    /**
     * Retrieves the token from the local storage.
     * @returns {string} The token.
     */
    getToken() {
        return window.localStorage.getItem("token");
    },
    /**
     * Saves the token in the local storage.
     * @param {string} token - The token to be saved.
     */
    saveToken(token) {
        window.localStorage.setItem("token", token);
    },
};