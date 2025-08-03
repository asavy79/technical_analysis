import axios from "axios";


const axiosInstance = axios.create({
    baseUrl: "localhost:8000",
    headers: {
        "Content-Type": "application/json",
    }
});

export default axiosInstance