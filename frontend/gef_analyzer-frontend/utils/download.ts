import axios from "axios";

export async function download_csv() {
  try {
    const response = await axios.get("/api/download");

    const blob = new Blob([response.data], { type: "text/csv" });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = "exported_data.csv";
    link.click();
    URL.revokeObjectURL(url);
  } catch (error) {
    console.error("An error occurred:", error);
  }
}
