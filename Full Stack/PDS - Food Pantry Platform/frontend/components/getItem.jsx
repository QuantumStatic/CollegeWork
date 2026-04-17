import { useEffect, useState } from "react";
import axios from "axios";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { unescapeHTML } from "./utils";

import "../styles/get-item.css";

export function GetItem() {
  const [itemID, setItemID] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState();
  const [itemData, setItemData] = useState({
    iDescription: "",
    color: "",
    material: "",
    isNew: "",
    hasPieces: "",
    itemCategory: "",
    itemSubCategory : ""
  });
  const [itemPieces, setItemPieces] = useState([]);
  const [itemIamge, setItemImage] = useState(null);

  const { state } = useLocation();
  const nav = useNavigate();

  const checkItemID = (itemID) => {
    const itemRegex = /^\d+$/;
    return itemRegex.test(itemID);
  };

  const handleClick = async () => {
    let isvalid = checkItemID(itemID);
    setLoading(true);
    setItemData({
      iDescription: "",
      color: "",
      material: "",
      isNew: "",
      hasPieces: "",
      itemCategory: "",
    });
    setItemPieces([]);
    setItemImage(null);
    setError(null);
    if (isvalid) {
      try {
        const response = await axios.get(
          `http://127.0.0.1:5000/api/getitem/${itemID}`,
          {
            withCredentials: true,
          }
        );
        setItemData((currentState) => ({
          ...currentState,
          iDescription: response.data.iDescription,
          material: response.data.material ? response.data.material : "",
          color: response.data.color ? response.data.color : "",
          itemCategory: response.data.Category,
          itemSubCategory : response.data.subCategory,
          isNew: !!response.data.isNew,
          hasPieces: !!response.data.hasPieces,
        }));

        setItemPieces(response.data.pieces);

        setItemImage(`data:image/jpeg;base64,${response.data.photo}`);
      } catch (error) {
        console.log("error", error.response.data.error);
        setError(error.response.data.error);
      } finally {
        setLoading(false);
      }
    } else {
      setLoading(false);
      setError("Invalid Item Id");
    }
  };

  useEffect(() => {
    if (state) {
      const itemId = state.toString();
      setItemID(itemId);
    }
  }, [state]);

  useEffect(() => {
    if(state) {
      const handleClickAsync = async () => {
        await handleClick();
      };
      handleClickAsync();
    }
  }, [itemID]);

return (
  <>
    <div className="header-container">
      {!state ? (
        <Link to="/" className="home-link">Home</Link>
      ) : (
        <Link onClick={() => nav(-1)} className="back-link">Back</Link>
      )}
      <div id="page-title">Search Items</div>
    </div>


    <div className="input-container">
      <label htmlFor="item" className="item-label"></label>
      <input
        type="text"
        value={itemID}
        placeholder="Enter ItemID"
        onChange={(e) => setItemID(e.target.value)}
        disabled={!!state}
        className="item-input"
      />
      <button 
        onClick={handleClick} 
        disabled={!!state} 
        className="get-item-button"
      >
        {loading ? "Loading..." : "Search"}
      </button>
    </div>
    
    {error && <div className="error-message">{error}</div>}

    {itemData.itemCategory && itemData.iDescription && (
      <div className="item-details-container">
        <div className="item-description">Item Description: {unescapeHTML(itemData.iDescription)}</div>
        <div className="item-category">Category: {itemData.itemCategory}</div>
        <div className="item-color">Item Color: {unescapeHTML(itemData.color)}</div>
        <div className="item-category">Category: {itemData.itemCategory}</div>
        <div className="item-sub-category">Sub-Category: {itemData.itemSubCategory}</div>
        <div className="item-material">Item Material: {unescapeHTML(itemData.material)}</div>
        <div className="item-is-new">Item is New: {itemData.isNew ? <>Yes</> : <>No</>}</div>
        <div className="item-has-pieces">
          Item has more than 1 Piece: {itemData.hasPieces ? <>Yes</> : <>No</>}
        </div>
        <br />
        <div className="pieces-title">Pieces:</div>
        {itemPieces.map((piece, index) => (
          <div key={index} className="piece-container">
            <div className="piece-number">Piece Number: {piece.pieceNum}</div>
            <div className="piece-description">Piece Description: {unescapeHTML(piece.pDescription)}</div>
            <div className="piece-location">
              Piece Location:
              <div className="room-number">Room Number: {piece.roomNum}</div>
              <div className="shelf-number">Shelf Number: {piece.shelfNum}</div>
            </div>
            <br />
          </div>
        ))}
      </div>
    )}

    {itemIamge && <img src={itemIamge} alt="Item" className="item-image" />}
  </>
);
}
