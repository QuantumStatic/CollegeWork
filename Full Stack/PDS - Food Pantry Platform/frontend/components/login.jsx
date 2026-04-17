import { useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { sanitizeInput } from "./utils";

import "../styles/login.css";
import "../styles/home-button.css";

export function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [passwordVisible, setPasswordVisible] = useState(false);
  const nav = useNavigate();

  const disabled = !username || !password;

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);

    const formData = new FormData();
    formData.append("username", sanitizeInput(username));
    formData.append("password", password);

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/api/login",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          withCredentials: true,
        }
      );

      if (response.data.message === "Login successful") {
        nav("/");
      }
    } catch (error) {
      setError(error.response.data.error);
    } finally {
      setLoading(false);
    }
  };


  const togglePasswordVisibility = () => {
    setPasswordVisible(!passwordVisible);
  };

  return (
    <>
      <Link to="/" className="home-link">Home</Link>
      <div className="login-container">
        <div className="page-title">Log In</div>
        <form onSubmit={handleSubmit} className="login-form" action="/login">
          <div className="form-group">
            <label htmlFor="username" className="form-label">Username</label>
            <input
              type="text"
              name="username"
              autoComplete="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="form-input"
              required
            />

          </div>
          <div className="form-group">
            <label htmlFor="password" className="form-label">Password</label>
            <input
              type={passwordVisible ? "text" : "password"}
              name='password'
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="form-input"
              required
            />
            <span
                className="toggle-password"
                onClick={togglePasswordVisibility}
              >
                {passwordVisible ? "🙈" : "👁️"}
              </span>
          </div>
          <button
            className="login-button"
            type="submit"
            disabled={disabled || loading}
          >
            {loading ? "Logging In..." : "Login"}
          </button>
          {error && <div className="error-message">{error}</div>}
          <Link to="/register" className="register-link">Not a user? Sign Up Instead</Link>
        </form>
      </div>
    </>
  );
}