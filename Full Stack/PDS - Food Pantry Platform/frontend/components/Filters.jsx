import { useEffect, useState } from "react";
import axios from "axios";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { unescapeHTML } from "./utils";
import { useContext } from "react";
import { OrderContext } from "./orderContext";

import "../styles/filters.css";

export function Filter() {
  const { state } = useLocation();
  const [fetchResponse, setFetchResponse] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [next, setNext] = useState(false);
  const [prev, setPrev] = useState(false);
  const [page, setPage] = useState(1)

  const { items, addItem, client } = useContext(OrderContext);
  const [isStaff, setIsStaff] = useState(false);
  const nav = useNavigate();

  useEffect(() => {
    const checkStaff = async () => {
      try {
        await axios.get(`http://127.0.0.1:5000/api/check/staff`, {
          withCredentials: true,
        });
        setIsStaff(true);
      } catch (error) {
        if (error.response) {
          setIsStaff(false);
        } else {
          nav("/");
        }
      }finally {
        setLoading(false)
      }
    };
    checkStaff(); 
  }, [])

  useEffect(() => {
    const fetchItems = async (formData) => {
      try {
        const response = await axios.post(
          `http://127.0.0.1:5000/api/category/${page}`,
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
            withCredentials: true,
          }
        );

        setFetchResponse(response.data.result);
        response.data.next === 1 ? setNext(true) : setNext(false)
        response.data.prev === 1 ? setPrev(true) : setPrev(false)

      } catch (error) {
        if (error.response) {
          setError(error.response.data.error);
        } else {
          nav("/");
        }
      }finally {
        setLoading(false);
      }
    };

    if (state) {
      const formData = new FormData();
      formData.append("data", JSON.stringify(state));
      fetchItems(formData);
    } else {
      const formData = new FormData();
      formData.append("data", JSON.stringify({}));
      fetchItems(formData);
    }
  }, [state, page]);

  if (loading) {
    return <div>Loading...</div>
  }


  return (
  <div className="filters-container">
    <div className="navigation-bar">
      <Link to="/" className="nav-button">Home</Link>
      <Link to="/order" className="nav-button">Cart</Link>
      <Link to="/categories" className="nav-button">Select Categories</Link>
    </div>

    <h3 className="items-header">Items</h3>

    {error && <div className="error-message">{error}</div>}

    {fetchResponse && (
      <div className="items-list">
        {fetchResponse.map((item) => (
          <div key={item.ItemID} className="item-card">
            {isStaff && client && (
              <div className="add-to-cart-container">
                <button
                  onClick={() => addItem(item.ItemID)}
                  disabled={items.includes(item.ItemID)}
                  className="add-to-cart-button"
                >
                  Add to cart
                </button>
              </div>
            )}
            <div className="item-container">
              <div className="item-description">
                Item Description: {unescapeHTML(item.iDescription)}
              </div>
              <div className="item-image-categories">
                <img src={`data:image/jpeg;base64,${item.photo}`} alt="Item" />
              </div>
              <div className="more-info">
                <a
                  onClick={() => nav("/get-item", { state: item.ItemID })}
                  className="more-info-link"
                >
                  Get More Info..
                </a>
              </div>
            </div>
          </div>
        ))}
      </div>
    )}

    <div className="pagination">
      {prev && (
        <button onClick={() => setPage((currentPage) => currentPage - 1)} className="pagination-button">
          Prev
        </button>
      )}
      {next && (
        <button onClick={() => setPage((currentPage) => currentPage + 1)} className="pagination-button">
          Next
        </button>
      )}
    </div>
  </div>
);
}
