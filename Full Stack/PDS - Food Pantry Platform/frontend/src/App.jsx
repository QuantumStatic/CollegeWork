import { useEffect, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import { Logout } from "../components/logout";
import validator from "validator";
// import LoadingAnimation from "../components/Loading";

import "../styles/App.css";
import "../styles/auth-button.css";

function App() {
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [loggedIn, setLoggedIn] = useState(false);
  const [error, setError] = useState(false);
  const [permission, setPermission] = useState(false);

  const getUser = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/api/profile", {
        withCredentials: true,
      });
      return response.data;
    } catch (error) {
      if (error.response && error.response.data) {
        return error.response.data;
      } else {
        setError("Server Not Found");
        return { error: "" };
      }
    }
  };

  const checkStaff = async () => {
    try {
      await axios.get(`http://127.0.0.1:5000/api/check/staff`, {
        withCredentials: true,
      });
      setPermission(true);
    } catch (error) {
      if (error.response) {
        setPermission(false);
      }
    }
  };

  const logoutfunction = (logout) => {
    setLoggedIn(logout);
    setUserData("User");
  };

  useEffect(() => {
    const fetchUserData = async () => {
      const result = await getUser();

      if (result.error) {
        setUserData("User");
        setLoggedIn(false);
      } else {
        setUserData(result.fname);
        setLoggedIn(true);
        await checkStaff();
      }
      setLoading(false);
    };
    fetchUserData();
  }, []);

  const unescapeHTML = (input) => {
    return validator.unescape(input); // Unescape HTML entities like &lt; -> <
  };

  if (loading) {
    return <div>Loading...</div>;
  }
  if (error) {
    return <div>Server Not Found</div>;
  }

  return (
    <div className="app-container">
      {!loggedIn ? (
        <div className="welcome-container">
          <div className="welcome-message">Welcome, User</div>
          <div className="centered-button">
            <Link to="/login" className="auth-button">Login</Link>
          </div>
        </div>
      ) : (
        <div className="logged-in-layout">
          <div className="top-bar">
            <div className="welcome-container">
              <span className="welcome-message">Welcome, {unescapeHTML(userData)}</span>
            </div>
            <div className="home-title">Home</div>
            <div className="logout-container">
              <Logout logout={logoutfunction} />
            </div>
          </div>
          <div className="menu-container">
            <div className="menu">
              <Link to="/profile" className="menu-item">My Profile</Link>
              <Link to="/get-item" className="menu-item">Get Item</Link>
              <Link to="/order-details" className="menu-item">Order Details</Link>
              <Link to="/order-history" className="menu-item">Your Order History</Link>
              <Link to="/categories" className="menu-item">Categories</Link>
              {permission && <Link to="/donate" className="menu-item">New Donation</Link>}
              {permission && <Link to="/order" className="menu-item">New Order</Link>}
              {permission && <Link to="/ranking" className="menu-item">Volunteer Ranking</Link>}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;