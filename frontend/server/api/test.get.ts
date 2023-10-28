import axios from "axios";

export default defineEventHandler(async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8888/lorem");
    // console.log(response.data);
    return response.data; // Return the data obtained from the API call
  } catch (error) {
    console.error("There was an error making the GET request:", error);
    throw error; // Rethrow the error to be caught by the caller
  }
});
