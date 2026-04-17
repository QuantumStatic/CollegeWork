import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";
import { sanitizeInput } from "./utils";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { useContext } from "react";
import { OrderContext } from "./orderContext";

// import "../styles/Order.css";


export function Orders() {
  const [isStaff, setIsStaff] = useState(false);
  const [isClient, setIsClient] = useState(false);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const { items, addItem, addClient, client, deleteAll, orderDetail, addOrderDetails } = useContext(OrderContext);
  const nav = useNavigate();

  const [orderData, setOrderData] = useState({
    client: "",
    orderNotes: orderDetail.orderNotes,
    orderDate: new Date(),
    deliveredBy: orderDetail.deliveredBy,
    deliveryDate: orderDetail.deliveredDate,
    deliveredStatus: orderDetail.deliveredStatus,
  });

  const empty = {
    client: "",
    orderNotes: "",
    orderDate: new Date(),
    deliveredBy: "",
    deliveryDate: "",
    deliveredStatus: "New Order",
  }
  
  useEffect(() => {
    const checkStaff = async () => {
      try {
        await axios.get(`http://127.0.0.1:5000/api/check/staff`, {
          withCredentials: true,
        });

        setIsStaff(true);
      } catch (error) {
        console.log(error);
        if (error.response) {
          setError(error.response.data.error);
        } else {
          nav("/");
        }
      }
    };
    checkStaff();

    if (client) {
      setOrderData((currentState) => ({
        ...currentState,
        client: client
      }))
      setIsClient(true);
    }

  }, []);

  const checkClient = async (e) => {
    e.preventDefault();
    if (orderData.client.length > 0) {
      try {
        await axios.get(
          `http://127.0.0.1:5000/api/check/client/${sanitizeInput(
            orderData.client
          )}`,
          {
            withCredentials: true,
          }
        );
        setIsClient(true);
        addClient(orderData.client)
      } catch (error) {
        setIsClient(false);

        if (error.response) {
          setError(error.response.data.error);
        } else {
          nav("/");
        }
      }
    }
  };

  const checkDelivery = () => {
    if (orderData.deliveredBy === orderData.client){
      setError('client and delivery partner cannot be same');
      return false;
    } else {
      setError(null);
      return true;
    }
  }




  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setResult("");
    setError(null)

    if (orderData.client && orderData.orderDate && orderData.deliveryDate && orderData.deliveredBy && checkDelivery()) {
      const itemIDs = items;
      const orderDate = new Date(orderData.orderDate).toISOString().split("T")[0];
      const deliveryDate = new Date(orderData.deliveryDate).toISOString().split("T")[0];
      const formData = new FormData();
      formData.append("username", sanitizeInput(orderData.client));
      formData.append("orderNotes", sanitizeInput(orderData.orderNotes));
      formData.append("orderDate", orderDate);
      formData.append("deliveredBy", sanitizeInput(orderData.deliveredBy));
      formData.append("deliveredDate", deliveryDate);
      formData.append("deliveredStatus", sanitizeInput(orderData.deliveredStatus));
      formData.append("itemID", itemIDs);

      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/api/createorder",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
            withCredentials: true,
          }
        );
        setResult(response.data.message);
        setOrderData(empty)
        setIsClient(false)
        deleteAll();
        

      } catch (error) {
        setError(error.response.data.error);
      } finally {
        setLoading(false);
      }
    }else{
        setLoading(false);
    }
  };

  useEffect(() => {
    addOrderDetails('orderNotes' , orderData.orderNotes)
    addOrderDetails('deliveredBy', orderData.deliveredBy)
    addOrderDetails('deliveredDate', orderData.deliveryDate)
    addOrderDetails('deliveredStatus', orderData.deliveredStatus)
  }, [orderData])

  if (!isStaff) {
    return (
      <div>
        <Link to="/">Home</Link>
        <div>{error}</div>
      </div>
    );
  }

  return (
  <>
    <Link to="/" className="">Home</Link>
    <form onSubmit={handleSubmit} className="order-form">
      <div className="client-section">
        <label htmlFor="client" className="form-label">Client</label>
        <input
          type="text"
          className="input-client"
          value={orderData.client}
          onChange={(e) =>
            setOrderData((currentState) => ({
              ...currentState,
              client: e.target.value,
            }))
          }
          required
        />
        <button onClick={(e) => checkClient(e)} className="btn-enter-client">Enter Client</button>
      </div>
      <br />
      {isClient && (
        <>
          <div className="order-details">
            <div className="form-group">
              <label htmlFor="orderNotes" className="form-label">Order Notes</label>
              <input
                type="text"
                className="input-order-notes"
                value={orderData.orderNotes}
                onChange={(e) =>
                  setOrderData((currentState) => ({
                    ...currentState,
                    orderNotes: e.target.value,
                  }))
                }
                disabled = {items.length == 0}
              />
            </div>
            <br />
            <div className="form-group">
              <label htmlFor="orderDate" className="form-label">Order Date</label>
              <DatePicker
                selected={orderData.orderDate}
                className="datepicker-order-date"
                onChange={(date) =>
                  setOrderData((currentState) => ({
                    ...currentState,
                    orderDate: date,
                  }))
                }
                required
                disabled = {true}
              />
            </div>
            <br />
            <div className="form-group">
              <label htmlFor="deliveredBy" className="form-label">Delivery Partner Username</label>
              <input
                type="text"
                className="input-delivered-by"
                value={orderData.deliveredBy}
                onChange={(e) =>
                  setOrderData((currentState) => ({
                    ...currentState,
                    deliveredBy: e.target.value,
                  }))
                }
                required
                disabled = {items.length == 0}
              />
            </div>
            <br />
            <div className="form-group">
              <label htmlFor="deliveryDate" className="form-label">Delivery Date</label>
              <DatePicker
                selected={orderData.deliveryDate}
                className="datepicker-delivery-date"
                placeholderText="MM/DD/YYYY"
                onChange={(date) =>
                  setOrderData((currentState) => ({
                    ...currentState,
                    deliveryDate: date,
                  }))
                }
                minDate={orderData.orderDate}
                required
                disabled = {items.length == 0}
              />
            </div>
            <br />
            <div className="form-group">
              <label htmlFor="deliveryStatus" className="form-label">Delivery Status</label>
              <input
                type="text"
                className="input-delivery-status"
                value={orderData.deliveredStatus}
                onChange={(e) =>
                  setOrderData((currentState) => ({
                    ...currentState,
                    deliveredStatus: e.target.value,
                  }))
                }
                disabled = {items.length == 0}
                required
              />
            </div>
          </div>
          <br />
          <div className="order-items">
            <div className="order-items-header">Order Items</div>
            {items.map((field, index) => {
              return (
                <div key={index} className="order-item">
                  <label htmlFor={`item-${index}`} className="item-label">Item: {field}</label>
                  <a onClick={() => addItem(field)} className="item-delete-link">Delete</a>
                  <br />
                </div>
              );
            })}
            <div className="add-item-link">
              <a onClick={() => nav('/categories')}>Add Item</a>
            </div>
          </div>
          <button type="submit" className="btn-submit-order">
            {!loading ? "Register" : "Sending"}
          </button>
        </>
      )}
      <br />
    </form>
    {result && <div className="result-message">{result}</div>}
    {error && <div className="error-message">{error}</div>}
  </>
);
}
