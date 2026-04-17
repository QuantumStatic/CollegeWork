import { useEffect, useState } from "react";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";
import validator from "validator";
import { unescapeHTML } from "./utils";

export function SupervisionTasks() {
  const [staffName, setStaffName] = useState("");
  const [loading, setLoading] = useState(true);
  const [permission, setPermission] = useState(true);
  const [error, setError] = useState();
  const [data, setdata] = useState([]);
  const nav = useNavigate();

  const checkName = (userName) => {
    return validator.escape(userName);
  };

  useEffect(() => {
    const checkStaff = async () => {
      try {
        await axios.get(`http://127.0.0.1:5000/api/check/staff`, {
          withCredentials: true,
        });

      } catch (error) {
        if (error.response) {
          setPermission(false);
        } else {
          nav("/");
        }
      }finally {
        setLoading(false)
      }
    };
    checkStaff();
  }, []);

  const handleClick = async () => {
    setLoading(true);
    setError(null);
    setdata(null);
    if (staffName.length > 0) {
        try {
            const response = await axios.get(
              `http://127.0.0.1:5000/api/tasks/supervision/${checkName(staffName)}`,
              {
                withCredentials: true,
              }
            );

            setdata(response.data);

          } catch (error) {
              console.log(error);
              if (error.response) {
                  setError(error.response.data.error);
              }else {
                  nav("/")
              }
            
          } finally {
            setLoading(false);
          }
    } else {
        setError('Enter a Valid Name');
        setLoading(false);
    }
    
  };

  if (loading) {
    return <div>Loading...</div>
  }

  return (
    <>
      <Link to="/">Home</Link>
      {permission ? (
        <>
          <div>
            <label htmlFor="staffName"></label>
            <input
              type="text"
              value={staffName}
              placeholder="Enter Name"
              onChange={(e) => setStaffName(e.target.value)}
            />
            <button onClick={handleClick}>
              {loading ? "Loading..." : "Get Tasks"}
            </button>
          </div>

          {error && <div>{error}</div>}

          {data && (
            <div>
              {data.map((task) => {
                return (
                  <div key={task.orderID}>
                    <div>Order ID: {task.orderID}</div>
                    <div>Client : {unescapeHTML(task.client)}</div>
                    <div>Date : {task.orderDate}</div>
                    <div>Notes : {unescapeHTML(task.orderNotes)}</div>
                    <br />
                  </div>
                );
              })}
            </div>
          )}
        </>
      ) : (
        <div>You Do Not Have Permission to Access This</div>
      )}
    </>
  );
}
