import React, { useState } from "react";

import axios from "axios";

const HotelSearch = () => {
  const [hotelName, setHotelName] = useState("");
  const [hotelData, setHotelData] = useState(null);
  const [message, setMessage] = useState("");

  const API_URL = "http://localhost:8000"; // backend URL

  const fetchHotelData = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/hotels/scrape?hotel_name=${hotelName}`);
      console.log("API response:", response.data);
      setHotelData(response.data);
      setMessage("");
    } catch (error) {
      console.error("Error searching hotel.", error);
      setHotelData(null);
      setMessage("Error searching hotel.");
    }
  };

  const handleSave = async () => {
    if (!hotelData) {
      setMessage("No hotel data to save.");
      return;
    }

    try {
      const dataToSend = {
        name: hotelData.name,
        address: hotelData.address,
        description: hotelData.description,
        review: parseFloat(hotelData.review),
      };

      console.log("Data to send", dataToSend);

      const response = await axios.post(`${API_URL}/api/hotels`, dataToSend);

      console.log("Backend response", response.data);
      setMessage("Data saved successfully.");
    } catch (error) {
      console.error("Error saving data.", error);
      setMessage("Error saving data.");
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>Search Hotel</h1>
      {/* Field to insert Hotel name */}
      <input
        type="text"
        placeholder="Type hotel name..."
        value={hotelName}
        onChange={(e) => setHotelName(e.target.value)}
        style={{ padding: "10px", width: "300px", marginRight: "10px" }}
      />
      {/* Search button */}
      <button
        onClick={fetchHotelData}
        style={{ padding: "10px 20px", cursor: "pointer", backgroundColor: "#007BFF", color: "white", border: "none" }}
      >
        Search
      </button>

      {/* Hotel data */}
      {hotelData && (
        <div style={{ marginTop: "20px", padding: "10px", border: "1px solid #ccc", borderRadius: "5px" }}>
          <h2>Hotel info</h2>
          <p><strong>Name:</strong> {hotelData.name}</p>
          <p><strong>Address:</strong> {hotelData.address}</p>
          <p><strong>Description:</strong> {hotelData.description}</p>
          <p><strong>Review:</strong> {hotelData.review}</p>
          {/* Save button */}
          <button
            onClick={handleSave}
            style={{ padding: "10px 20px", cursor: "pointer", backgroundColor: "#28a745", color: "white", border: "none" }}
          >
            Save
          </button>
        </div>
      )}

      {/* Error or success message */}
      {message && <p style={{ color: "#d9534f", marginTop: "20px" }}>{message}</p>}
    </div>
  );
};

export default HotelSearch;
