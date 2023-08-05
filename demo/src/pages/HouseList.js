import styles from "./HouseList.module.css";
import OneHouse from "../components/HouseList/OneHouse.js";
import React, { useState, useEffect } from "react";
import { ReactComponent as CheckedImg } from "../assets/Main/checkedImg.svg";
import { Link } from "react-router-dom";

function HouseList({ houseData, setSelectedHouse }) {
  const [checked, setChecked] = useState(false);
  const [goodHouses, setGoodHouses] = useState([]);

  useEffect(() => {
    const filteredHouses = houseData.filter(
      (house) => house.suggest_ratio >= 0.5
    );
    setGoodHouses(filteredHouses);
  }, [checked]);

  const handleCheckboxClick = () => {
    setChecked((prevChecked) => !prevChecked);
  };

  return (
    <div className={styles.div}>
      <div className={styles.checkBox}>
        <div className={styles.checkBoxDiv} onClick={handleCheckboxClick}>
          <div className={styles.checkBoxRectangle}>
            {checked && <CheckedImg className={styles.checked} />}
          </div>
          <span className={styles.checkBoxText}>추천 비율 높은 집만 보기</span>
        </div>
      </div>

      <div className={styles.houseList}>
        {checked
          ? goodHouses.map((house, index) => {
              if (house !== null) {
                return (
                  <Link to=":houseId">
                    <span
                      key={index}
                      className={styles.oneHouseMargin}
                      onClick={() => setSelectedHouse(house)}
                    >
                      <OneHouse house={house}></OneHouse>
                    </span>
                  </Link>
                );
              } else {
                return null;
              }
            })
          : houseData.map((house, index) => (
              <Link to=":houseId">
                <span
                  key={index}
                  className={styles.oneHouseMargin}
                  onClick={() => setSelectedHouse(house)}
                >
                  <OneHouse house={house}></OneHouse>
                </span>
              </Link>
            ))}
      </div>
    </div>
  );
}

export default HouseList;
