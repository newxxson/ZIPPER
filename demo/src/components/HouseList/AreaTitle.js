import styles from "./AreaTitle.module.css";

const areaTitles = {
  Anam: "참살이길",
  Gangnam: "개운사길",
  Mapo: "법학관 후문",
  Other: "제기동",
};

function AreaTitle({ areaName, userLike }) {
  return (
    <span
      className={styles.areaButton}
      style={{ borderColor: userLike ? "red" : "#b7b7b7" }} // 동적으로 테두리 색상 변경
    >
      {areaName}
    </span>
  );
}

export default AreaTitle;
