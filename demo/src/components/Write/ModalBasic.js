import styles from './ModalBasic.module.css';
import JusoPopup from "./JusoPopup";

function ModalBasic({ setModalOpen, onReturnValue, onClose}) {
    // 모달 끄기 
    const closeModal = () => {
        setModalOpen(false);
    };

    return (
        <span className={styles.container}>
            <span className={styles.close} onClick={closeModal}>
                X  
            </span>
            <JusoPopup onClose={onClose} onReturnValue={onReturnValue} />   
                     
            
        </span>
    );
}

export default ModalBasic;
