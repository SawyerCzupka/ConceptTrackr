import axios from "axios";

export default defineEventHandler(async () => {
  try {
    const response = await axios.request({
      url: "http://127.0.0.1:8888/testFileDownload",
      responseType: "arraybuffer",
    });

    return new Blob([response.data], { type: "text/csv" }); // Return the data obtained from the API call
  } catch (error) {
    console.error("An error occurred:", error);
    throw error; // Rethrow the error to be caught by the caller
  }
});
