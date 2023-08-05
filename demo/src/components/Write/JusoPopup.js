// Popup.js
import React, { useState } from "react";
import $ from "jquery";
import styles from "./jusoPopup.module.css"; //

const JusoPopup = ({ onClose, onReturnValue }) => {
  const [keyword, setKeyword] = useState("");
  const [results, setResults] = useState([]);

  function checkSearchedWord(obj) {
    if (obj.length > 0) {
      // 특수문자 제거

      var expText = /[%=><]/;

      if (expText.test(obj) == true) {
        alert("특수문자를 입력 할수 없습니다.");

        obj = obj.split(expText).join("");

        return false;
      }

      // 특정문자열(sql예약어의 앞뒤공백포함) 제거

      var sqlArray = new Array(
        "OR",
        "SELECT",
        "INSERT",
        "DELETE",
        "UPDATE",
        "CREATE",

        "DROP",
        "EXEC",
        "UNION",
        "FETCH",
        "DECLARE",
        "TRUNCATE"
      );

      // sql 예약어

      var regex = "";

      for (var num = 0; num < sqlArray.length; num++) {
        regex = new RegExp(sqlArray[num], "gi");

        if (regex.test(obj.value)) {
          alert(
            '"' + sqlArray[num] + '"와(과) 같은 특정문자로 검색할 수 없습니다.'
          );

          obj.value = obj.value.replace(regex, "");

          return false;
        }
      }
    } else {
      alert("주소를 입력해주세요!");
      return false;
    }
    return true;
  }

  function getAddr() {
    // 적용예 (api 호출 전에 검색어 체크)
    if (!checkSearchedWord(keyword)) {
      return;
    }

    $.ajax({
      url: "http://www.juso.go.kr/addrlink/addrLinkApiJsonp.do",

      type: "POST",

      data: {
        confmKey: "	devU01TX0FVVEgyMDIzMDgwMzE3NDQ0NzExMzk4ODc=",

        currentPage: 1,

        countPerPage: 10,

        keyword: keyword,

        resultType: "json",
      },

      dataType: "jsonp",

      crossDomain: true,

      success: function (jsonStr) {
        setResults(jsonStr.results.juso);
      },
      error: function (xhr, status, error) {
        alert("에러발생");
      },
    });
  }
  const handleInputChange = (e) => {
    setKeyword(e.target.value);
  };
  const handleReturnClick = () => {
    onClose();
  };
  const handleJusoClick = (result) => {
    onReturnValue(result.roadAddr);
    onClose();
  };
  return (
    <div className={styles.contents}>
      <h2>■ 행정안전부 - 주소 검색 API</h2>
      <hr />

      <input
        type="text"
        value={keyword}
        onChange={handleInputChange}
        placeholder="  도로명주소, 건물명 또는 지번 입력"
      />
      <div className={styles.searchBtn}>
        <button onClick={getAddr}>
          <h4>주소검색</h4>
        </button>
      </div>

      <div className={styles.results_container}>
        <ul>
          <div className={styles.li_container}>
            {results.map((result) => (
              <li
                key={result.zipNo}
                onClick={() => {
                  handleJusoClick(result);
                }}
              >
                <div className={styles.content_wrapper}>{result.roadAddr}</div>
              </li>
            ))}
          </div>
        </ul>
      </div>
    </div>
  );
};

export default JusoPopup;
