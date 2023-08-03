import React, { useState, useEffect } from "react";
import Form1 from "./Form1";
import Keywordselect from "./Keywordselect";
import TextReview from "./TextReview";
import ShowRating from "./ShowRating";
import ShowReview from "./ShowReview";
import { prettyDOM } from "@testing-library/react";

const App = () => {
  const [step, setStep] = useState(1);
  const [form1Data, setForm1Data] = useState(null);
  const [keywordData, setKeywordData] = useState(null);
  const [textReviewData, setTextReviewData] = useState(null);
  const [ratingData, setRatingData] = useState(null);
  const token = "a9ab0d9ff961ee340d675a187ac5bea9f7f86342";

  const wrapUp = (data) => {
    setRatingData((prevData) => ({
      ...prevData,
      ...data,
    }));
    setStep((prevStep) => prevStep + 1);
  };

  const handleNext = (data) => {
    if (step === 1) {
      setForm1Data(data);
      console.log();
    } else if (step === 2) {
      setKeywordData(data);
      console.log("testing", keywordData);
    } else if (step === 3) {
      setTextReviewData(data);
    } else if (step === 4) {
      setRatingData(data);
    }
    setStep((prev) => prev + 1);
  };

  const handlePrev = () => {
    setStep((prevStep) => prevStep - 1);
  };

  return (
    <div>
      {step === 1 && <Form1 onNext={handleNext} form1Data={form1Data} />}
      {step === 2 && (
        <Keywordselect
          onNext={handleNext}
          onPrev={handlePrev}
          keywordData={keywordData}
        />
      )}
      {step === 3 && (
        <TextReview
          onNext={handleNext}
          onPrev={handlePrev}
          textReviewData={textReviewData}
        />
      )}
      {step === 4 && (
        <ShowRating
          onPrev={handlePrev}
          onNext={wrapUp}
          ratingData={ratingData}
        />
      )}
      {step === 5 && (
        <ShowReview
          token={token}
          data={{ form1Data, keywordData, textReviewData, ratingData }}
        />
      )}
    </div>
  );
};

export default App;

