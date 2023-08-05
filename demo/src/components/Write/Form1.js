import React, { useState, useEffect } from "react";
import styles from "./Form1.module.css"; //
import { ReactComponent as Car } from "../../assets/Write/Car.svg";
import Popup from "./JusoPopup";
import JusoPopup from "./JusoPopup";
import ModalBasic from "./ModalBasic";

function generateYearOptions(startYear, endYear) {
  const yearOptions = [];
  for (let year = startYear; year <= endYear; year++) {
    yearOptions.push(
      <option key={year} value={year}>
        {year}년
      </option>
    );
  }
  return yearOptions;
}

const Form1 = ({ onNext, form1Data }) => {
  // 상태(state) 변수들을 정의합니다.
  const [floor, setFloor] = useState(""); // 거주 층수
  const [moveOutYear, setMoveOutYear] = useState(""); // 퇴실 연도
  const [residenceType, setResidenceType] = useState(""); // 거주 유형
  const [deposit, setDeposit] = useState(""); // 보증금
  const [monthlyRent, setMonthlyRent] = useState(""); // 월세
  const [maintenance, setMaintenance] = useState(""); // 관리비
  const [address, setAddress] = useState(""); // 주소
  const [name, setName] = useState("");
  const [area, setArea] = useState(""); // 지역
  const [popup, setPopup] = useState(false);
  const [RentType, setRentType] = useState("");

  // 페이지가 로드될 때 또는 form1Data가 변경될 때 실행되는 부분입니다.
  useEffect(() => {
    // form1Data가 있으면 해당 데이터로 상태(state)를 초기화합니다.
    if (form1Data) {
      setFloor(form1Data.floor); // 거주 층수
      setMoveOutYear(form1Data.moveOutYear); // 퇴실 연도
      setResidenceType(form1Data.residenceType); // 거주 유형
      setDeposit(form1Data.deposit); // 보증금
      setMonthlyRent(form1Data.monthlyRent); // 월세
      setMaintenance(form1Data.maintenance); // 관리비
      setAddress(form1Data.address); // 주소
      setArea(form1Data.area); // 지역
      setRentType(form1Data.RentType);
    }
  }, [form1Data]);

  // 폼 제출 시 호출되는 함수입니다.
  const handleSubmit = (e) => {
    e.preventDefault();
    // 입력된 폼 데이터를 객체로 만듭니다.

    const formData = {
      floor, // 거주 층수
      moveOutYear, // 퇴실 연도
      residenceType, // 거주 유형
      deposit, // 보증금
      monthlyRent, // 월세
      maintenance, // 관리비
      address, // 주소
      area, // 지역
      name,
      RentType,
    };
    // 다음 페이지로 데이터를 넘깁니다.
    onNext(formData);
  };

  const onClose = () => {
    setPopup(false);
  };
  const onPopup = (e) => {
    e.preventDefault();

    setPopup(true);
  };
  const onReturnValue = (data) => {
    setAddress(data);
  };

  return (
    <div className={styles.formDiv}>
      <form className={styles.formContainer} onSubmit={handleSubmit}>
        <div className={styles.fomContainerDiv}>
          <label>
            <h1>기본 정보 입력</h1>
            <h2>주소</h2>
            <span className={styles.SearchInput}>
              <input
                type="text"
                placeholder="주소찾기 버튼을 클릭해주세요!"
                value={address}
              />
              <div className={styles.SearchWrapper}>
                <button
                  className={`${styles.addressSearch} ${styles.buttonStyle}`}
                  onClick={onPopup}
                >
                  <h4>주소 찾기</h4>
                </button>
              </div>
            </span>

            <h2>집 이름</h2>
            <input
              type="text"
              value={name}
              placeholder="건물이름을 입력해주세요! ex) 청암원룸"
              onChange={(e) => setName(e.target.value)}
            />
          </label>

          <label>
            <h2>지역</h2>
            <select value={area} onChange={(e) => setArea(e.target.value)}>
              <option disabled selected value="">
                어느 동네에 거주하시나요?
              </option>
              <option value="정후">정후</option>
              <option value="Anam-bub">법후</option>
              <option value="정문">정문</option>
              <option value="참살이">참살이</option>
              {/* Add more options for other regions as needed */}
            </select>
          </label>

          <label>
            <h2>거주 층수</h2>
            <select value={floor} onChange={(e) => setFloor(e.target.value)}>
              <option disabled selected value="">
                {" "}
                저층, 중층, 상층 중 선택하세요!
              </option>
              <option value="UP">상</option>
              <option value="MID">중</option>
              <option value="LOW">하</option>
            </select>
          </label>

          <label>
            <h2>퇴실연도</h2>
            <select
              value={moveOutYear}
              onChange={(e) => setMoveOutYear(e.target.value)}
            >
              <option disabled selected value="">
                {" "}
                연도를 입력해주세요!
              </option>
              {generateYearOptions(2015, 2023)}
            </select>
          </label>
          <label>
            <h2>계약 유형</h2>
            <select value={area} onChange={(e) => setRentType(e.target.value)}>
              <option disabled selected value="">
                월세, 전세 중 선택해주세요!
              </option>
              <option value="월세">월세</option>
              <option value="전세">전세</option>
            </select>
          </label>

          <label>
            <h2>거주 유형</h2>
            <select
              value={residenceType}
              onChange={(e) => setResidenceType(e.target.value)}
            >
              <option disabled selected value="">
                원룸, 오피스텔, 쉐어하우스 중 선택해주세요!
              </option>
              <option value="OpenOneRoom">원룸</option>
              <option value="오피스텔">오피스텔</option>
              <option value="쉐어하우스">쉐어하우스</option>
            </select>
          </label>
          <div className={styles.priceInputContainer}>
            <label>
              <h2>보증금</h2>
              <input
                placeholder="만원 단위"
                type="number"
                value={deposit}
                onChange={(e) => setDeposit(e.target.value)}
                className={styles.priceInput}
              />
            </label>
            <label>
              <h2>월세</h2>
              <input
                placeholder="만원 단위"
                type="number"
                value={monthlyRent}
                onChange={(e) => setMonthlyRent(e.target.value)}
                className={styles.priceInput}
              />
            </label>
            <label>
              <h2>관리비</h2>
              <input
                placeholder="만원 단위"
                type="number"
                value={maintenance}
                onChange={(e) => setMaintenance(e.target.value)}
                className={styles.priceInput}
              />
            </label>
          </div>
        </div>

        <div className={styles.bottom}>
          <div className={styles.buttonWrapper}>
            <button className={styles.buttonStyle} type="submit">
              <h3>NEXT</h3>
            </button>
          </div>
          <Car className={styles.bottomCar} />
          <div className={styles.bottomBox}>
            <h3>1단계</h3>
            <h4>진행 중...</h4>
          </div>
        </div>
      </form>
      {popup && (
        <div className={styles.modalBasicClass}>
          <ModalBasic
            setModalOpen={onClose}
            onClose={onClose}
            onReturnValue={onReturnValue}
          />
        </div>
      )}
    </div>
  );
};

export default Form1;
