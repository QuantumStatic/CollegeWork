import React, {createContext, useEffect, useState} from "react";

export const OrderContext = createContext();

export const OrderProvider = ({ children }) => {
  const [items, setItems] = useState([]);
  const [client, setClient] = useState(null)
  const [orderDetail, setOrderDetail] = useState({
    orderNotes : "",
    deliveredBy : "",
    deliveredDate : "",
    deliveredStatus : "New Order",
  })

  const addOrderDetails = (category, value) => {
    setOrderDetail((currentState) => ({...currentState, [category] : value}))
    return
  }
  const addItem = (itemID) =>
    setItems((currentContext) => {
      if (currentContext.includes(itemID)) {
        return currentContext.filter((item) => item !== itemID);
      } else {
        return [...currentContext, itemID];
      }
    });

    const deleteAll = () => {
      setItems([]);
      setClient(null);
      setOrderDetail((currentState) => ({
        ...currentState,
        orderNotes : "",
        deliveredBy : "",
        deliveredDate : "",
        deliveredStatus : "New Order",
      }))
      return
    }
  
    const addClient = (username) => setClient(username) 

  return (
    <OrderContext.Provider value={{ items, addItem, addClient, client, deleteAll, orderDetail, addOrderDetails }}>
      {children}
    </OrderContext.Provider>
  );
};
