export default {
    clear() {
        window.localStorage.clear()
    },
    getPlayerName() {		
        return window.localStorage.getItem("playerName");
    },
    savePlayerName(playerName) {
        window.localStorage.setItem("playerName", playerName);
    },
    getParticipationScore() {
        return window.localStorage.getItem("participationScore");
    },
    saveParticipationScore(participationScore) {
        window.localStorage.setItem("participationScore", participationScore);
    },
    getToken() {
        return window.localStorage.getItem("token");
    },
    saveToken(token) {
        window.localStorage.setItem("token", token);
    },
};