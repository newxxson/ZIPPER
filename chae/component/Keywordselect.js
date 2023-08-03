import React, { useState, useEffect } from "react";
import styles from './Keywordselect.module.css';
import {ReactComponent as Car} from "../assets/Car.svg";

const Keywordselect = ({ onNext, onPrev, keywordData }) => {
  const [selectedOption, setSelectedOption] = useState("");
  const [selectedKeywords, setSelectedKeywords] = useState([]);
  const [keywordOptions, setKeywordOptions] = useState({});

  useEffect(() => {
    if (keywordData) {
      setSelectedOption(keywordData.selectedOption);
      setSelectedKeywords(keywordData.selectedKeywords);
    }
  }, [keywordData]);

  useEffect(() => {
    console.log("Current state:", keywordOptions);
  }, [keywordOptions]);

  const getKeywords = () => {
    fetch(
      "http://ec2-13-125-213-208.ap-northeast-2.compute.amazonaws.com:8000/api/keywords/",{
        method: "GET",
        mode: "cors",
      }
    )
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok.");
        }
        return response.json();
      })
      .then((jsonData) => {
        setKeywordOptions({ ...jsonData });
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  };

  useEffect(() => {
    getKeywords();
  }, []); // Empty dependency array to run only once on component mount

  const handleOptionChange = (e) => {
    const option = e.target.value;
    setSelectedOption(option);
  };

  const handleKeywordSelect = (keyword) => {
    if (selectedKeywords.includes(keyword)) {
      setSelectedKeywords(selectedKeywords.filter((kw) => kw !== keyword));
    } else {
      setSelectedKeywords([...selectedKeywords, keyword]);
    }
  };

  const handleNext = () => {
    const data = {
      selectedOption,
      selectedKeywords,
    };
    onNext(data);
  };

  const handlePrev = () => {
    onPrev();
  };

  return (
    <div className={styles.keywordselectContainer}>
      <h1>해당되는 키워드를 선택해주세요!</h1>
      <select value={selectedOption} onChange={handleOptionChange}>
        <option value="">옵션 선택</option>
        {Object.keys(keywordOptions).map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>

      {selectedOption && keywordOptions[selectedOption] ? (
        <div>
          <h2>{selectedOption}</h2>
          <ul>
            {keywordOptions[selectedOption].map((keyword) => (
              <li
                key={keyword.pk}
                onClick={() => handleKeywordSelect(keyword)}
                style={{
                  fontWeight: selectedKeywords.includes(keyword)
                    ? "bold"
                    : "normal",
                }}
              >
                {keyword.description}
              </li>
            ))}
          </ul>
        </div>
      ) : (
        <div></div>
      )}

      <h2>선택한 키워드</h2>
      <ul>
        {selectedKeywords.map((keyword) => (
          <li key={keyword.pk}>{keyword.description}</li>
        ))}
      </ul>


      
      <div className={styles.bottom}>      
      <div className={styles.buttonWrapper}>
      <button onClick={handlePrev}><h3>BACK</h3></button>
      <button onClick={handleNext}><h3>NEXT</h3></button></div>
      <div></div>
      <Car />
      <div className={styles.bottomBox}>
        <h3>2단계</h3>
        <h4>진행 중...</h4>
      </div></div>
    </div>
    
  );
};

export default Keywordselect;
