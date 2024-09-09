import React from "react";
import Modal from "react-modal";
import styles from './LoadingModal.module.scss';

Modal.setAppElement('#root'); // Required for accessibility

interface LoadingModalProps {
  isOpen: boolean;
  onRequestClose: () => void;
}

const LoadingModal: React.FC<LoadingModalProps> = ({ isOpen, onRequestClose }) => {
  return (
    <Modal
      isOpen={isOpen}
      onRequestClose={onRequestClose}
      contentLabel="Loading"
      className={styles.modal}
      overlayClassName={styles.overlay}
    >
      <div className={styles.loadingContent}>
        <p>Loading...</p>
        {/* You can add a spinner or any other loading indicator here */}
      </div>
    </Modal>
  );
};

export default LoadingModal;
