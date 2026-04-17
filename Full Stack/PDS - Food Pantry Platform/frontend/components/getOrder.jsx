import { useEffect, useState } from "react";
import axios from "axios";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { unescapeHTML } from "./utils";

import "../styles/get-order.css";

export function GetOrder() {
  const [updatePermission, setUpdatePermission] = useState(false);
  const [doUpdate, setDoUpdate] = useState(false);
  const [orderID, setorderID] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState();
  const [orderClient, setOrderClient] = useState(null);
  const [orderDate, setorderDate] = useState(null);
  const [orderItems, setOrderItems] = useState([]);
  const [orderDelivery, setOrderDelivery] = useState({
    deliverdBy: "",
    date: "",
    status: "",
  });

  const { state } = useLocation();
  const nav = useNavigate();
  const [suerpvisor, setSupervisor] = useState(null);

  const checkOrderID = (itemID) => {
    const itemRegex = /^\d+$/;
    return itemRegex.test(itemID);
  };

  const handleClick = async () => {
    let isvalid = checkOrderID(orderID);
    setOrderDelivery({
      deliverdBy: "",
      date: "",
      status: "",
    });
    setSupervisor(null);
    setLoading(true);
    setOrderClient(null);
    setorderDate(null);
    setOrderItems(null);
    setError(null);

    if (isvalid) {
      try {
        const response = await axios.get(
          `http://127.0.0.1:5000/api/order/${orderID}`,
          {
            withCredentials: true,
          }
        );
        setOrderClient(response.data.client);
        setorderDate(response.data.orderDate);
        setOrderItems(response.data.item);
        setOrderDelivery((curretState) => ({
          ...curretState,
          deliverdBy: response.data.delivery_partner,
          date: response.data.delivery_date,
          status: response.data.status,
        }));
        setSupervisor(response.data.supervisor);
      } catch (error) {
        console.log(error);
        setError(error.response.data.error);
      } finally {
        setLoading(false);
      }
    } else {
      setLoading(false);
      setError("Invalid Order Id");
    }
  };

  useEffect(() => {
    if (state) {
      const orderID = state.toString();
      setorderID(orderID);
    }

    const checkUser = async () => {
      try {
        await axios.get(`http://127.0.0.1:5000/api/check/user`, {
          withCredentials: true,
        });
        setUpdatePermission(true);
      } catch (error) {
        error.response ? setUpdatePermission(false) : nav("/");
      }
    };
    checkUser();
  }, [state]);

  useEffect(() => {
    if (state) {
      const handleClickAsync = async () => {
        await handleClick();
      };
      handleClickAsync();
    }
  }, [orderID]);

  const handleUpdate = async(event) => {
    event.preventDefault();
    try {
      const formData = new FormData();
      formData.append("stauts", orderDelivery.status);
      formData.append("orderID", orderID);
      const response = await axios.post(
        "http://127.0.0.1:5000/api/status-update",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          withCredentials: true,
        }
      );
        setDoUpdate(false)
    } catch (error) {
      console.log(error);
        error.response ? setError(error.response.data.error) : nav("/")
    }
  }

return (
  <>
    {/* Navigation Bar */}
    <div className="top-bar">
      {!state ? (
        <Link to="/" className="home-link">Home</Link>
      ) : (
        <Link onClick={() => nav(-1)} className="back-link">Back</Link>
      )}
      <h1 id="page-title-get-order">Order Details</h1>
    </div>

    {/* Search Bar */}
    <div className="search-bar">
      <label htmlFor="order" className="search-label"></label>
      <input
        type="text"
        value={orderID}
        placeholder="Enter OrderID"
        onChange={(e) => setorderID(e.target.value)}
        disabled={!!state}
        className="search-input"
      />
      <button onClick={handleClick} disabled={!!state} className="search-button">
        {loading ? "Loading..." : "Get Item"}
      </button>
    </div>

    {error && <div className="error-message">{error}</div>}
    <br />

    {/* Order and Items Section */}
    {orderClient && orderDate && (
      <div className="order-page">
        <div className="client-info-container">
          <h2 className="client-info-title">Client Info</h2>
          <div className="order-info-card">
            <p><strong>Client:</strong> {unescapeHTML(orderClient)}</p>
            <p><strong>Order Date:</strong> {orderDate}</p>
            <p><strong>Supervisor:</strong> {suerpvisor}</p>
            <p><strong>Delivery Partner:</strong> {orderDelivery.deliverdBy}</p>
            <p><strong>Delivery Date:</strong> {orderDelivery.date}</p>
            {doUpdate ? (
              <div className="delivery-status-update">
                <span><strong>Delivery Status:</strong></span>
                <input
                  type="text"
                  value={orderDelivery.status}
                  onChange={(e) => setOrderDelivery((state) => ({ ...state, status: e.target.value }))}
                  className="status-input"
                />
                <button onClick={(e) => handleUpdate(e)} className="update-button">Update</button>
              </div>
            ) : (
              <div className="delivery-status-display">
                <p><strong>Delivery Status:</strong> {orderDelivery.status}</p>
                {updatePermission && (
                  <button onClick={() => setDoUpdate((state) => !state)} className="toggle-update-button">
                    Update
                  </button>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Items Section */}
        <div className="items-container">
          <h2 className="items-title">Items</h2>
          {orderItems.map((item) => (
            <div key={item.ItemID} className="item-card">
              <p><strong>Item ID:</strong> {item.ItemID}</p>
              <p><strong>Item Description:</strong> {unescapeHTML(item.iDescription)}</p>
              <div className="pieces-container">
                {item.piece.map((pie) => (
                  <div key={pie.pieceNum} className="piece-card">
                    <p><strong>Piece Number:</strong> {pie.pieceNum}</p>
                    <p><strong>Piece Description:</strong> {unescapeHTML(pie.pDescription)}</p>
                    <p><strong>Piece Location:</strong></p>
                    <ul>
                      <li><strong>Room Number:</strong> {pie.roomNum}</li>
                      <li><strong>Shelf Number:</strong> {pie.shelfNum}</li>
                    </ul>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    )}
  </>
);
}
