import React, { useState, useEffect } from 'react';

const API_BASE_URL = "http://localhost:1700";

const MerchantDashboard = () => {
  const [merchant, setMerchant] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const merchantId = "de0d16d46040497787250f6b237eabe2"; 

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/merchant/${merchantId}`)
      .then(response => response.json())
      .then(data => {
        console.log("API Response:", data); 
        if (data && data.success) {
          setMerchant(data.merchant);
        } else {
          throw new Error("Invalid API response structure");
        }
      })
      .catch(error => {
        console.error("Error fetching merchant:", error);
        setError(error.message);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) return <h3>Loading Merchant Data...</h3>;
  if (error) return <h3 style={{ color: "red" }}>Error: {error}</h3>;
  if (!merchant) return <h3>No Merchant Data Found</h3>;

  return (
    <div>
      <h2>Merchant Dashboard</h2>
      <p><strong>Name:</strong> {merchant.name}</p>
      <p><strong>Business Type:</strong> {merchant.business_type}</p>
      <p><strong>Location:</strong> {merchant.location}</p>
      <p><strong>Email:</strong> {merchant.email}</p>
      <p><strong>Phone:</strong> {merchant.phone}</p>
      <p><strong>Payment Method:</strong> {merchant.payment_method}</p>
    </div>
  );
};

export default MerchantDashboard;
