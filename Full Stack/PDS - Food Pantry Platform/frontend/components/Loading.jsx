import React from "react";
import "../styles/Loading.css";

const LoadingAnimation = () => {
  return (
    <div className="loading-container">
      <div className="loading-animation">
        <div className="circle-wrapper">
          <div className="circle circle-1"></div>
          <div className="circle circle-2"></div>
          <div className="circle circle-3"></div>
        </div>
        <div className="text">Loading</div>
        <div className="text-glitch">Loading</div>
      </div>
    </div>
  );
};

export default LoadingAnimation;