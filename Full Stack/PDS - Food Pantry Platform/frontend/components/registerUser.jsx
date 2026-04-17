import { useState } from "react";
import axios from "axios";
import validator from "validator";
import { Link, useNavigate } from "react-router-dom";

import "../styles/home-button.css";
import "../styles/registerUser.css";

export function RegisterUser() {
  const [userName, setUserName] = useState("");
  const [password, setPasssword] = useState("");
  const [fname, setFname] = useState("");
  const [lname, setLaname] = useState("");
  const [email, setEmail] = useState("");
  const [role, setRole] = useState({
    Client: false,
    Donator: false,
    Staff: false,
    Volunteer: false,
  });
  const [loading, setLoading] = useState(false);
  const [Error, setError] = useState("");
  const [phoneFields, setPhoneFields] = useState([{ id: 1, value: "" }]);
  const [result, setResult] = useState(null);
  const nav = useNavigate();

  function sanitizeInput(input) {
    return validator.escape(input);
  }

  const isPhoneNumber = (value) => {
    const phoneRegex = /^\d{10,12}$/;
    return phoneRegex.test(value);
  };

  const isEmail = (value) => {
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    return emailRegex.test(value);
  };

  const validatePhoneNumbers = () => {
    let validationError = null;

    phoneFields.forEach((phone) => {
      if (!isPhoneNumber(phone.value)) {
        validationError = `Phone number with ID ${phone.id} is invalid.`;
      }
    });

    if (validationError) {
      setError(validationError);
      return false;
    } else {
      setError("");
      return true;
    }
  };

  const validateEmail = () => {
    let validationError = null;
    if (!isEmail(email)) {
      validationError = `Email is invalid.`;
    }

    if (validationError) {
      setError(validationError);
      return false;
    } else {
      return true;
    }
  };

  const validateRoles = (roles) => {
    if (roles.length < 1) {
      setError("No Role Selected");
      return false;
    } else {
      return true;
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setResult("");

    const isValidPhone = validatePhoneNumbers();
    const isValidEmail = validateEmail();
    let roles = [];
    role.Client ? roles.push("Client") : null;
    role.Donator ? roles.push("Donator") : null;
    role.Volunteer ? roles.push("Volunteer") : null;
    role.Staff ? roles.push("Staff") : null;

    const checkRoles = validateRoles(roles);
    if (isValidPhone && isValidEmail && checkRoles) {
      const phoneNumbers = phoneFields.map((field) => field.value);
      const formData = new FormData();
      formData.append("username", sanitizeInput(userName));
      formData.append("password", password);
      formData.append("fname", sanitizeInput(fname));
      formData.append("lname", sanitizeInput(lname));
      formData.append("email", sanitizeInput(email));
      formData.append("role", roles);
      formData.append("phone", phoneNumbers);

      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/api/register",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
            withCredentials: true,
          }
        );
        setResult(response.data.message);
      } catch (error) {
        setError(error.response.data.error);
      } finally {
        setLoading(false);
      }
    } else {
      setLoading(false);
    }
  };

  const addPhoneField = () => {
    setPhoneFields((currentstate) => [
      ...currentstate,
      { id: currentstate.length + 1, value: "" },
    ]);
  };

  const removePhoneField = (id) => {
    setPhoneFields(phoneFields.filter((field) => field.id !== id));
  };

  const onPhoneChange = (id, value) => {
    setPhoneFields(
      phoneFields.map((field) => (field.id == id ? { ...field, value } : field))
    );
  };

  return (
  <div className="register-container">
    <Link className="home-link" to="/">Home</Link>
    <div className="page-title">Sign Up</div>
    {result !== "User Registered Successfully" && (
      <form onSubmit={handleSubmit} className="register-form">
        <div className="form-group">
          <label htmlFor="username">Username</label>
          <input
            type="text"
            value={userName}
            placeholder="Set Username"
            onChange={(e) => setUserName(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            value={password}
            placeholder="Set Password"
            onChange={(e) => setPasssword(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="fname">First Name</label>
          <input
            type="text"
            placeholder="Set First Name"
            value={fname}
            onChange={(e) => setFname(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="lname">Last Name</label>
          <input
            type="text"
            placeholder="Set Last Name"
            value={lname}
            onChange={(e) => setLaname(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            type="text"
            placeholder="Set Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div className="form-group roles-group">
          <div>
            <input
              type="checkbox"
              onChange={(e) =>
                setRole((currentstate) => ({
                  ...currentstate,
                  Client: !role.Client,
                }))
              }
              checked={role.Client}
            />
            <label htmlFor="Client">Client</label>
          </div>

          <div>
            <input
              type="checkbox"
              onChange={(e) =>
                setRole((currentstate) => ({
                  ...currentstate,
                  Donator: !role.Donator,
                }))
              }
              checked={role.Donator}
            />
            <label htmlFor="Donator">Donator</label>
          </div>

          <div>
            <input
              type="checkbox"
              onChange={(e) =>
                setRole((currentstate) => ({
                  ...currentstate,
                  Volunteer: !role.Volunteer,
                }))
              }
              checked={role.Volunteer}
            />
            <label htmlFor="Volunteer">Volunteer</label>
          </div>

          <div>
            <input
              type="checkbox"
              onChange={(e) =>
                setRole((currentstate) => ({
                  ...currentstate,
                  Staff: !role.Staff,
                }))
              }
              checked={role.Staff}
            />
            <label htmlFor="Staff">Staff</label>
          </div>
        </div>

        <div className="form-group phone-group">
          {phoneFields.map((field) => (
            <div key={field.id} className="phone-field">
              <label htmlFor={`phone-${field.id}`}>Phone {field.id}</label>
              <input
                type="text"
                placeholder={`Set Phone ${field.id}`}
                id={`phone-${field.id}`}
                value={field.value}
                onChange={(e) => onPhoneChange(field.id, e.target.value)}
              />
              {field.id == phoneFields.length && field.id != 1  && (
                <a
                  className="delete-phone"
                  onClick={() => removePhoneField(field.id)}
                >
                  Delete
                </a>
              )}
            </div>
          ))}
          <div className="add-phone">
            <a onClick={addPhoneField}>Add Phone</a>
          </div>
        </div>

        <button type="submit" className="register-button">
          {!loading ? "Register" : "Sending"}
        </button>
      </form>
    )}

    {Error && <div className="error-message">{Error}</div>}
    {result && <div className="result-message">{result}</div>}
    {result == "User Registered Successfully" && (
      <Link to="/login" className="login-link">Go to Login</Link>
    )}
  </div>
);
}