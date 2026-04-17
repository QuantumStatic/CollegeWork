import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import { unescapeHTML } from "./utils";

import "../styles/order-history.css";

export function OrderHistory() {
  const [client, setClient] = useState(null);
  const [orders, setOrders] = useState([]);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState(['Client', 'Supervisor', 'Delivery-Partner'])
  const [loading, setLoading] = useState(true);
  const nav = useNavigate();

  useEffect(() => {
    const orderHistory = async () => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:5000/api/orderhistory",
          {
            withCredentials: true,
          }
        );

        setClient(response.data.client);
        setOrders(response.data.orders);
        console.log(response.data.orders);
      } catch (error) {
        if (error.response && error.response.data.error == 'User not logined'){
            nav("/login")
        }
        else if (error.response){
            setError(error.response.data.error)
        }
        else{
            nav("/")
        }
            
      }finally{
        setLoading(false)
      }
    };
    orderHistory();
  }, []);

  const roleFilter = (value) => {
    setFilter(currentState => (currentState.includes(value) ? currentState.filter(val => val !== value) : [...currentState, value]))
  }

  if (loading) {
    return <div>Loading...</div>
  }


return (
  <>
    <div className="order-history-header">
      <Link to="/" className="home-link">Home</Link>
      <h3 className="order-history-title">Order History</h3>
    </div>

    {client && (
      <div className="filters-container">
        <div className="filter-item">
          <input
            type="checkbox"
            id="filter-client"
            onChange={(e) => roleFilter('Client')}
            checked={filter.includes('Client')}
            className="filter-checkbox"
          />
          <label htmlFor="filter-client" className="filter-label">Client</label>
        </div>
        <div className="filter-item">
          <input
            type="checkbox"
            id="filter-supervisor"
            onChange={(e) => roleFilter('Supervisor')}
            checked={filter.includes('Supervisor')}
            className="filter-checkbox"
          />
          <label htmlFor="filter-supervisor" className="filter-label">Supervisor</label>
        </div>
        <div className="filter-item">
          <input
            type="checkbox"
            id="filter-delivery"
            onChange={(e) => roleFilter('Delivery-Partner')}
            checked={filter.includes('Delivery-Partner')}
            className="filter-checkbox"
          />
          <label htmlFor="filter-delivery" className="filter-label">Delivery Partner</label>
        </div>
      </div>
    )}

    {client ? (
      <div className="orders-container">
        <div className="user-info">
          <span className="user-label">User:</span> {client}
        </div>
        <hr className="separator" />
        {orders.map((order) => {
          return (
            (filter.includes(order.as[0]) || filter.includes(order.as[1]) || filter.includes(order.as[2])) && (
              <div key={order.orderId} className="order-item">
                <div className="order-info">
                  <span className="order-id">Order Id:</span> {order.orderId}
                </div>
                <div className="order-info">
                  <span className="order-date">Order Date:</span> {order.orderDate}
                </div>
                <div className="order-info">
                  <span className="order-as">As:</span> {
                    order.as.map((as) => ((as.length > 0) && (<span>{as} </span>) ))
                  }
                </div>
                <div className="order-items">
                  {order.items.map((item) => (
                    <div key={item.ItemID} className="order-item-details">
                      <div className="item-info">
                        <span className="item-id">ItemID:</span> {item.ItemID}
                      </div>
                      <div className="item-info">
                        <span className="item-description">Item Description:</span> {unescapeHTML(item.iDescription)}
                      </div>
                    </div>
                  ))}
                </div>
                <div className="more-info">
                  <a
                    onClick={() => nav("/order-details", { state: order.orderId })}
                    className="more-info-link"
                  >
                    Get More Info..
                  </a>
                </div>
                <hr className="separator" />
              </div>
            )
          );
        })}
      </div>
    ) : (
      <div className="error-message">{error}</div>
    )}
  </>
);
}