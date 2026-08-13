"use client";

import Modal from "@/components/common/Modal";
import UploadForm from "./UploadForm";

export default function UploadDialog({
  isOpen,
  onClose,
}) {
  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Upload Dataset"
    >
      <UploadForm onClose={onClose} />
    </Modal>
  );
}