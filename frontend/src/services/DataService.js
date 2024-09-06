import { BASE_API_URL } from "./Common";

const axios = require('axios');

const DataService = {
    Init: function () {
        // Any application initialization logic comes here
    },
    SaveAudio: async function (formData) {
        return await axios.post(BASE_API_URL + "/saveaudio", formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
    },
    GetInputAudios: async function () {
        return await axios.get(BASE_API_URL + "/input_audios");
    },
    DeleteAudio: async function (path) {
        return await axios.delete(BASE_API_URL + "/audio_data?path=" + path);
    },
}

export default DataService;