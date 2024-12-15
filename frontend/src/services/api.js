import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const fetchHotelData = async (hotelName) => {
    try {
        const response = await axios.get(`${API_URL}/api/hotels/scrape?hotel_name=${hotelName}`);
        console.log("API response", response.data);
        //setHotelData(response.data); //
      } catch (error) {
        console.error("Error searching hotel", error);
        if (error.response) {
          console.error("API response error.", error.response);
        } else if (error.request) {
          console.error("No response received", error.request);
        } else {
          console.error("Error request config", error.message);
        }
      }
};

export const saveHotelData = async (hotelData) => {
  try {
    const response = await axios.post(`${API_URL}/api/hotels`, hotelData);
    console.info(response.data);
    return response.data;
  } catch (error) {
    console.error("Error saving hotel data:", error);
    throw error;
  }
};
