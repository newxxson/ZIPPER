import { ReactComponent as GoodButtonImg } from "../../assets/Main/goodButtonImg.svg";
import React from "react";

const ButtonStyle = {
  border: "2px solid #4CAF50",
  padding: "0.2vh 0.6vw",
  borderRadius: "5px",
  display: "flex",
  flexDirection: "row",
  alignItems: "center",
  justifyContent: "center",
  width: "fit-content",
  boxShadow: "1px 1px 1px 0 rgba(0, 0, 0, 0.25)",
};

const ButtonTextStyle = {
  color: "#4CAF50",
  fontWeight: 700,
  marginLeft: "0.3vw",
  fontSize: "1vw",
};

function GoodButton() {
  return (
    <div style={ButtonStyle}>
      <GoodButtonImg fill="#4CAF50" />
      <span style={ButtonTextStyle}>추천</span>
    </div>
  );
}

export default GoodButton;
