import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { unescapeHTML } from "./utils";
import { Link } from "react-router-dom";
import "../styles/userProfile.css";

export function UserPorfile() {
  const [userName, setUserName] = useState("");
  const [fname, setFname] = useState(null);
  const [lname, setLname] = useState(null);
  const [email, setuserEmail] = useState(null);
  const [phone, setPhone] = useState([]);
  const [loading, setLoading] = useState(true);
  const [result, setResult] = useState(null);
  const [addPhone, setAddPhone] = useState(false);
  const [newPhone, setNewPhone] = useState("");
  const [deletePhone, setDeletePhone] = useState(false)
  
  const nav = useNavigate();


  const isPhoneNumber = (value) => {
    const phoneRegex = /^\d{10,12}$/;
    return phoneRegex.test(value);
  };

  const validatePhoneNumber = () => {
    let validationError = null;

    if (!isPhoneNumber(newPhone)) {
      validationError = `Phone number is invalid.`;
    }

    if (validationError) {
      setResult(validationError);
      return false;
    } else {
      setResult("");
      return true;
    }
  };

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/profile", {
        withCredentials: true,
      });
      if (response) {
        setUserName(response.data.username);
        setFname(response.data.fname);
        setLname(response.data.lname);
        setuserEmail(response.data.email);
        setPhone(response.data.phone);
        setLoading(false);
      } else {
        nav("/");
      }
      } catch (error) {
        nav("/")
      }
    };
    setLoading(true)
    fetchUser();
  }, [userName]);

  const handleSubmitPhone = async (event) => {
    event.preventDefault();
    setResult(null);
    const isValidPhone = validatePhoneNumber();

    if (isValidPhone) {
      const formData = new FormData();
      formData.append("phone", newPhone);

      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/api/phone/add",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
            withCredentials: true,
          }
        );
        if (response.data.message) {
          setResult(response.data.message);
          setUserName("");
          setNewPhone("");
          setAddPhone(false)
        }
      } catch (error) {
        setResult(error.response.data.error);
      }
    }
  };

  const handleDeletePhone = async(event, number) => {
    event.preventDefault();
    setResult(null);

    const formData = new FormData();
    formData.append("phone", number);


    try {
        const response = await axios.post(
          "http://127.0.0.1:5000/api/phone/remove",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
            withCredentials: true,
          }
        );
        if (response.data.message) {
          setResult(response.data.message);
          setUserName("");
        }
      } catch (error) {
        setResult(error.response.data.error);
      }
  }

  if (loading) {
    return <div>Loading...</div>;
  }

return (
  <>
    <Link to="/" className="home-link">Home</Link>
    <div className="profile-container">
      <div className="profile-header">Your Profile</div>
      <div className="profile-username">Username: {unescapeHTML(userName)}</div>
      <div className="profile-name">
        Name: {unescapeHTML(fname)}, {unescapeHTML(lname)}
      </div>
      <div className="profile-email">Email: {unescapeHTML(email)}</div>
      <div className="profile-phones">
        {phone.map((number, index) => (
          <div key={index} className="phone-item">
            <div>
              Phone {index + 1}: {number}
              {deletePhone && (
                <button
                  className="delete-phone-button"
                  onClick={(e) => handleDeletePhone(e, number)}
                >
                  Delete
                </button>
              )}
            </div>
          </div>
        ))}
      </div>

      <button
        className="toggle-delete-phone-button"
        onClick={() => setDeletePhone((currentState) => !currentState)}
      >
        Delete Phone
      </button>
      <button
        className="toggle-add-phone-button"
        onClick={() => setAddPhone((currentState) => !currentState)}
      >
        {!addPhone ? <div>Add New Phone</div> : <div>Remove New Phone</div>}
      </button>

      {addPhone && (
        <div className="add-phone-container">
          <label htmlFor="newPhone" className="new-phone-label">
            New Phone Number
          </label>
          <input
            type="text"
            id="newPhone"
            className="new-phone-input"
            value={newPhone}
            onChange={(event) => setNewPhone(event.target.value)}
          />
          <button
            className="add-phone-button"
            onClick={(e) => handleSubmitPhone(e)}
          >
            Add Phone
          </button>
        </div>
      )}
      {result && <div className="result-message">{result}</div>}
    </div>
  </>
);
}
