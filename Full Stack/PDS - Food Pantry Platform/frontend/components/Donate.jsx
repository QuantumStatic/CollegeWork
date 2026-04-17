import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";
import { sanitizeInput } from "./utils";

import "../styles/donate.css";

export function Donate() {
  const [itemData, setItemData] = useState({
    donor: "",
    iDescription: "",
    color: "",
    isNew: null,
    hasPieces: null,
    material: "",
    image: null,
  });
  const empty = [
    {
      donor: "",
      iDescription: "",
      color: "",
      isNew: null,
      hasPieces: null,
      material: "",
      image: null,
    },
    [
      {
        pieceNum: 1,
        pDescription: "",
        Length: "",
        width: "",
        height: "",
        roomNum: "",
        shelfNum: "",
        pNotes: "",
      },
    ],
  ];
  const [error, setError] = useState(null);
  const [isDonor, setIsDonor] = useState(false);
  const [isStaff, setIsStaff] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [disableTrue, setDisableTrue] = useState(false);
  const [imagePreview, setImagePreview] = useState(null);
  const [mainCategory, setMainCategory] = useState({
    options: [],
    selected: "",
  });
  const [subCategory, setSubCategory] = useState({
    options: [],
    selected: "",
  });
  const [pieceFields, setPieceFields] = useState([
    {
      pieceNum: 1,
      pDescription: "",
      Length: "",
      width: "",
      height: "",
      roomNum: "",
      shelfNum: "",
      pNotes: "",
    },
  ]);
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
          setError(error.response.data.error);
        } else {
          nav("/");
        }
      }
    };
    checkStaff();
  }, []);

  const checkDonor = async (e) => {
    setError(null)
    e.preventDefault();
    if (itemData.donor.length > 0) {
      try {
        await axios.get(
          `http://127.0.0.1:5000/api/check/donator/${sanitizeInput(
            itemData.donor
          )}`,
          {
            withCredentials: true,
          }
        );
        setDisableTrue(true)
        setIsDonor(true);
        try {
          const response = await axios.get(
            `http://127.0.0.1:5000/api/getcategory`,
            {
              withCredentials: true,
            }
          );

          setMainCategory((currentState) => ({
            ...currentState,
            options: response.data.categories.map((category) => {
              return category.category;
            }),
          }));

          setSubCategory((currentState) => ({
            ...currentState,
            options: response.data.categories.reduce((acc, obj) => {
              acc[obj.category] = obj.sub_category;
              return acc;
            }, {}),
          }));
        } catch (error) {
          console.log(error);
        }
      } catch (error) {
        setIsDonor(false);
        if (error.response) {
          setError(error.response.data.error);
        } else {
          nav("/");
        }
      }
    }
  };

  const handleCategoryChange = (e) => {
    setMainCategory((currentState) => ({
      ...currentState,
      selected: e.target.value,
    }));

    setSubCategory((currentState) => ({
      ...currentState,
      selected: "",
    }));
  };

  const addPieceField = () => {
    setPieceFields((currentstate) => [
      ...currentstate,
      {
        pieceNum: currentstate.length + 1,
        pDescription: "",
        Length: "",
        width: "",
        height: "",
        roomNum: "",
        shelfNum: "",
        pNotes: "",
      },
    ]);
  };

  const isNumber = (value) => {
    const phoneRegex = /^\d+(\.\d+)?$/;
    return phoneRegex.test(value);
  };

  const validateNumbers = () => {
    let validationError = null;

    pieceFields.forEach((piece) => {
      if (!isNumber(piece.Length)) {
        validationError = `Piece number with ID ${piece.pieceNum} has invalid Length`;
      } else if (!isNumber(piece.width)) {
        validationError = `Piece number with pieceNum ${piece.pieceNum} has invalid. wpieceNumth`;
      } else if (!isNumber(piece.height)) {
        validationError = `Piece number with pieceNum ${piece.pieceNum} has invalid. height`;
      } else if (!isNumber(piece.roomNum)) {
        validationError = `Piece number with pieceNum ${piece.pieceNum} has invalid. Room Number`;
      } else if (!isNumber(piece.roomNum)) {
        validationError = `Piece number with pieceNum ${piece.pieceNum} has invalid. Room Number`;
      } else if (!isNumber(piece.shelfNum)) {
        validationError = `Piece number with ID ${piece.pieceNum} has invalid. Shelf Number`;
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

  const removePieceField = (pieceNum) => {
    setPieceFields(pieceFields.filter((field) => field.pieceNum !== pieceNum));
  };

  const onPieceChange = (id, attribute, value) => {
    setPieceFields(
      pieceFields.map((field) =>
        field.pieceNum == id ? { ...field, [attribute]: value } : field
      )
    );
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null);
    const isValid = validateNumbers();
    if (
      isValid &&
      itemData.donor &&
      itemData.iDescription &&
      itemData.image &&
      mainCategory.selected &&
      subCategory.selected &&
      pieceFields &&
      itemData.isNew !== null &&
      itemData.hasPieces !== null
    ) {
      setLoading(true);
      const currentDate = new Date();
      const formattedDate = currentDate.toISOString().split("T")[0];
      const formData = new FormData();
      formData.append("donor", sanitizeInput(itemData.donor));
      formData.append("iDescription", sanitizeInput(itemData.iDescription));
      formData.append("color", sanitizeInput(itemData.color));
      formData.append("isNew", itemData.isNew);
      formData.append("hasPieces", itemData.hasPieces);
      formData.append("material", sanitizeInput(itemData.material));
      formData.append("mainCategory", mainCategory.selected);
      formData.append("subCategory", subCategory.selected);
      formData.append("donateDate", formattedDate);
      formData.append("photo", itemData.image);
      formData.append("pieces", JSON.stringify(pieceFields));
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/api/donate",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
            withCredentials: true,
          }
        );
        setResult(response.data.message);
        setImagePreview(null);
        setItemData(empty[0]);
        setMainCategory((currentState) => ({...currentState, selected : ""}))
        setSubCategory((currentState) => ({...currentState, selected : ""}))
        setPieceFields(empty[1]);
        setIsDonor(false);
      } catch (error) {
        console.log(error);
        if (error.response) {
          setError(error.response.data.error);
        } else {
          setError("Something Went Wrong / Some Requierd Fields Missing");
        }
      } finally {
        setLoading(false);
      }
    }
    setLoading(false);
  };

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    setError(null);

    if (!file) {
      setError("No File Selected");
      setItemData((currentState) => ({ ...currentState, image: null }));
      return;
    }

    if (file.size > 1024 * 1024) {
      setError("File size must be less than 1 MB");
      setItemData((currentState) => ({ ...currentState, image: null }));
      return;
    }
    setItemData((currentDate) => ({
      ...currentDate,
      image: file,
    }));

    const reader = new FileReader();
    reader.onload = () => {
      setImagePreview(reader.result);
    };
    reader.readAsDataURL(file);
  };

  if (!isStaff) {
    return (
      <div>
        <Link to="/">Home</Link>
        <div>{error}</div>
      </div>
    );
  }

  return (
  <div className="donate-container">
    <div className="donation-top-bar">
      <Link to="/" className="home-link">Home</Link>
      <h2 className="donation-title">Donation Form</h2>
    </div>
    <form onSubmit={handleSubmit} className="donate-form">
      <div className="form-group">
        <label htmlFor="donor" className="form-label">Donator</label>
        <input
          type="text"
          className="form-input"
          value={itemData.donor}
          onChange={(e) =>
            setItemData((currentState) => ({
              ...currentState,
              donor: e.target.value,
            }))
          }
          disabled = {disableTrue}
          required
        />
        <button onClick={(e) => checkDonor(e)} className="form-button">
          Enter Donor
        </button>
      </div>
      <br />
      {isDonor && (
        <div className="donor-details">
          <div className="form-group">
            <label htmlFor="iDescription" className="form-label">
              Item Description
            </label>
            <input
              type="text"
              className="form-input"
              value={itemData.iDescription}
              onChange={(e) =>
                setItemData((currentState) => ({
                  ...currentState,
                  iDescription: e.target.value,
                }))
              }
              required
            />
          </div>
          <br />
          <div className="form-group">
            <label htmlFor="color" className="form-label">Item Color</label>
            <input
              type="text"
              className="form-input"
              value={itemData.color}
              onChange={(e) =>
                setItemData((currentState) => ({
                  ...currentState,
                  color: e.target.value,
                }))
              }
            />
          </div>
          <div className="form-group">
            <div className="form-subgroup">
              <span className="form-text">Item Is New?</span>
              <label htmlFor="isNew" className="form-label">
                Yes
              </label>
              <input
                type="checkbox"
                className="form-checkbox"
                onChange={() =>
                  setItemData((currentState) => ({ ...currentState, isNew: 1 }))
                }
                checked={itemData.isNew == 1}
              />
              <label htmlFor="isNew" className="form-label">
                No
              </label>
              <input
                type="checkbox"
                className="form-checkbox"
                onChange={() =>
                  setItemData((currentState) => ({ ...currentState, isNew: 0 }))
                }
                checked={itemData.isNew == 0}
              />
            </div>
          </div>
          <div className="form-group">
            <div className="form-subgroup">
              <span className="form-text">Has Pieces (More than 1)</span>
              <label htmlFor="hasPieces" className="form-label">
                Yes
              </label>
              <input
                type="checkbox"
                className="form-checkbox"
                onChange={() =>
                  setItemData((currentState) => ({
                    ...currentState,
                    hasPieces: 1,
                  }))
                }
                checked={itemData.hasPieces == 1}
              />
              <label htmlFor="hasPieces" className="form-label">
                No
              </label>
              <input
                type="checkbox"
                className="form-checkbox"
                onChange={() =>
                  setItemData((currentState) => ({
                    ...currentState,
                    hasPieces: 0,
                  }))
                }
                checked={itemData.hasPieces == 0}
              />
            </div>
          </div>
          <div className="form-group">
            <label htmlFor="material" className="form-label">Item Material</label>
            <input
              type="text"
              className="form-input"
              value={itemData.material}
              onChange={(e) =>
                setItemData((currentState) => ({
                  ...currentState,
                  material: e.target.value,
                }))
              }
            />
          </div>
          <br />
          <div className="form-group">
            <label htmlFor="mainCategory" className="form-label">Category</label>
            <select
              id="mainCategory"
              className="form-select"
              value={mainCategory.selected}
              onChange={(e) => handleCategoryChange(e)}
            >
              <option value="">--Select--</option>
              {mainCategory.options.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </div>
          <br />
          <div className="form-group">
            <label htmlFor="subCategory" className="form-label">Sub Category</label>
            <select
              id="subCategory"
              className="form-select"
              value={subCategory.selected}
              onChange={(e) =>
                setSubCategory((currentState) => ({
                  ...currentState,
                  selected: e.target.value,
                }))
              }
              disabled={!mainCategory.selected}
            >
              <option value="">--Select--</option>
              {subCategory.options[mainCategory.selected]?.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </div>
          <br />
          <div className="pieces-container">
            <div className="form-text">Pieces</div>
            {pieceFields.map((field) => {
              return (
                <div key={field.pieceNum} className="piece-field">
                  <label htmlFor={`piece-${field.pieceNum}-pDescription`} className="form-label">
                    Piece Description
                  </label>
                  <input
                    type="text"
                    id={`piece-${field.pieceNum}-pDescription`}
                    className="form-input"
                    value={field.pDescription}
                    onChange={(e) =>
                      onPieceChange(field.pieceNum, "pDescription", e.target.value)
                    }
                    required
                  />
                  <br />
                  <label htmlFor={`piece-${field.pieceNum}-Length`} className="form-label">
                    Piece Length
                  </label>
                  <input
                    type="text"
                    id={`piece-${field.pieceNum}-Length`}
                    className="form-input"
                    value={field.Length}
                    onChange={(e) =>
                      onPieceChange(field.pieceNum, "Length", e.target.value)
                    }
                  />
                  <br />
                  <label htmlFor={`piece-${field.pieceNum}-width`} className="form-label">
                    Piece Width
                  </label>
                  <input
                    type="text"
                    id={`piece-${field.pieceNum}-width`}
                    className="form-input"
                    value={field.width}
                    onChange={(e) =>
                      onPieceChange(field.pieceNum, "width", e.target.value)
                    }
                  />
                  <br />
                  <label htmlFor={`piece-${field.pieceNum}-height`} className="form-label">
                    Piece Height
                  </label>
                  <input
                    type="text"
                    id={`piece-${field.pieceNum}-height`}
                    className="form-input"
                    value={field.height}
                    onChange={(e) =>
                      onPieceChange(field.pieceNum, "height", e.target.value)
                    }
                  />
                  <br />
                  <label htmlFor={`piece-${field.pieceNum}-roomNum`} className="form-label">
                    Piece Room Location
                  </label>
                  <input
                    type="text"
                    id={`piece-${field.pieceNum}-roomNum`}
                    className="form-input"
                    value={field.roomNum}
                    onChange={(e) =>
                      onPieceChange(field.pieceNum, "roomNum", e.target.value)
                    }
                    required
                  />
                  <br />
                  <label htmlFor={`piece-${field.pieceNum}-shelfNum`} className="form-label">
                    Piece Shelf Location
                  </label>
                  <input
                    type="text"
                    id={`piece-${field.pieceNum}-shelfNum`}
                    className="form-input"
                    value={field.shelfNum}
                    onChange={(e) =>
                      onPieceChange(field.pieceNum, "shelfNum", e.target.value)
                    }
                    required
                  />
                  <br />
                  <label htmlFor={`piece-${field.pieceNum}-pNotes`} className="form-label">
                    Piece Notes
                  </label>
                  <input
                    type="text"
                    id={`piece-${field.pieceNum}-pNotes`}
                    className="form-input"
                    value={field.pNotes}
                    onChange={(e) =>
                      onPieceChange(field.pieceNum, "pNotes", e.target.value)
                    }
                  />
                  {field.pieceNum !== 1 && (
                    <a
                      onClick={() => removePieceField(field.pieceNum)}
                      className="remove-piece-link"
                    >
                      Delete
                    </a>
                  )}
                  <br />
                  <br />
                </div>
              );
            })}
            <div>
              <a onClick={addPieceField} className="add-piece-link">
                Add Piece
              </a>
            </div>
          </div>
          <div className="form-group">
            <label htmlFor="image" className="form-label">
              Upload Image
            </label>
            <input
              type="file"
              className="form-input"
              accept="image/*"
              onChange={handleImageUpload}
              required
            />
            {imagePreview && (
              <div className="image-preview-container">
                <div className="image-preview-label">Image Preview</div>
                <img
                  src={imagePreview}
                  alt="Preview"
                  className="image-preview"
                />
              </div>
            )}
          </div>
          <button type="submit" className="submit-button">
            {!loading ? "Register" : "Sending"}
          </button>
        </div>
      )}
    </form>
    {error && <div className="error-message">{error}</div>}
    {result && <div className="result-message">{result}</div>}
  </div>
);
}
