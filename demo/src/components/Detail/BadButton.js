import { ReactComponent as BadButtonImg } from "../../assets/Main/badButtonImg.svg";

function BadButton() {
  const BadButtonStyle = {
    border: "2px solid #f44366",
    padding: "0.2vh 0.6vw",
    borderRadius: "5px",
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    width: "fit-content",
    boxShadow: "1px 1px 1px 0 rgba(0, 0, 0, 0.25)",
  };

  const BadButtonTextStyle = {
    color: "#f44366",
    fontWeight: 700,
    marginLeft: "0.3vw",
    fontSize: "1vw",
  };

  return (
    <span style={BadButtonStyle}>
      <BadButtonImg fill="#f44366" />
      <span style={BadButtonTextStyle}>비추</span>
    </span>
  );
}

export default BadButton;
