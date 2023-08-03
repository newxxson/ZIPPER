import React, { useState, useEffect } from "react";
import styles from './TextReview.module.css';
import {ReactComponent as Car} from "../assets/Car.svg";

  const TextReview = ({ onNext, onPrev, textReviewData }) => {
  const [satisfaction, setSatisfaction] = useState("");
  const [disappointment, setDisappointment] = useState("");
  const [residencePhoto, setResidencePhoto] = useState(null);
  const [residencePhotoPreview, setResidencePhotoPreview] = useState("");

  useEffect(() => {
    if (textReviewData) {
      setSatisfaction(textReviewData.satisfaction);
      setDisappointment(textReviewData.disappointment);
      if (textReviewData.residencePhoto) {
        setResidencePhotoPreview(
          URL.createObjectURL(textReviewData.residencePhoto)
        );
      }
    }
  }, [textReviewData]);

  const handleSatisfactionChange = (e) => {
    setSatisfaction(e.target.value);
  };

  const handleDisappointmentChange = (e) => {
    setDisappointment(e.target.value);
  };

  const handleResidencePhotoChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setResidencePhoto(file);
    }
    setResidencePhotoPreview(URL.createObjectURL(file));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const data = {
      satisfaction,
      disappointment,
      residencePhoto,
    };
    onNext(data);
  };

  const handlePrev = () => {
    onPrev();
  };

  return (
    <div className={styles.textReviewContainer}>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="satisfaction"><h1 style={{ color: 'red' }}>살아보고 만족스러웠던 Point</h1></label>
          <textarea
            id="satisfaction"
            value={satisfaction}
            onChange={handleSatisfactionChange}
          />
        </div>

        <div>
          <label htmlFor="disappointment"><h1 style={{ color: 'blue' }}>살아보고 실망스러웠던 Point</h1></label>
          <textarea
            id="disappointment"
            value={disappointment}
            onChange={handleDisappointmentChange}
          />
        </div>

        <div className={styles.customFileInput}>
          <label htmlFor="residencePhoto"><h1>거주 사진</h1></label>
        <input
          type="file"
          id="residencePhoto"
          accept="image/*"
          onChange={handleResidencePhotoChange}
        />
        {residencePhotoPreview && (
          <>
            <h1>선택한 사진:</h1>
            <img
              src={residencePhotoPreview}
              alt="Residence"
              style={{ width: "200px" }}
          
        />
        </>
      )}
      </div>
      </form>
      
      <div className={styles.bottom}>
      <div className={styles.buttonWrapper}>
      <button className={styles.button} onClick={handlePrev}><h3>BACK</h3></button>
      <button className={styles.button}type="submit" onClick={handleSubmit}><h3>NEXT</h3>
      </button>
      </div>
        <Car />
          <div className={styles.bottomBox}>
            <h3>3단계</h3>
            <h4>진행 중...</h4>
          </div>
      </div>
      </div>
  );
};

export default TextReview;
