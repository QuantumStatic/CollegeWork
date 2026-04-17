import { useState } from "react";
import axios from "axios";
import { useContext } from "react";
import { OrderContext } from "./orderContext";

import "../styles/auth-button.css";

export function Logout({ logout }) {
  const [loading, setLoading] = useState(false);
  const { deleteAll } = useContext(OrderContext);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);

    try {
      const response = await axios.get("http://127.0.0.1:5000/api/logout", {
        withCredentials: true,
      });
      deleteAll();
      logout(false);

    } catch (error) {
      console.log(error.response.data.error);
      
    } finally {
      setLoading(false);
    }
  };
  if (loading){
    return(
      <div>Loading...</div>
    )
    }
  return (
    <>
      <button className="logout-button" onClick={handleSubmit}>Logout</button>
    </>
  );
}
