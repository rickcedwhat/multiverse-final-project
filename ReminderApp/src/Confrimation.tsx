import React, { useState } from "react";
import {
  Stack,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
} from "@mui/material";

// Want to do something more imperative? Use a hook!

type useConfirmationProps = {
  message: string;
  onConfirm: () => void;
  onCancel?: () => void;
};

const useConfirmation = ({
  message,
  onConfirm,
  onCancel = () => {},
}: useConfirmationProps) => {
  const [isOpen, setIsOpen] = useState(false);

  const handleConfirm = () => {
    setIsOpen(false);
    onConfirm();
  };

  const handleCancel = () => {
    setIsOpen(false);
    onCancel();
  };

  const confirmation = (
    <Confirmation
      message={message}
      onConfirm={handleConfirm}
      onCancel={handleCancel}
      isOpen={isOpen}
    />
  );

  return { confirmation, showConfirmation: () => setIsOpen(true) };
};

type ConfirmationProps = {
  message: string;
  onConfirm: () => void;
  onCancel: () => void;
  isOpen: boolean;
};

const Confirmation = ({
  message,
  onConfirm,
  onCancel,
  isOpen,
}: ConfirmationProps) => {
  return (
    <Dialog open={isOpen}>
      <DialogTitle>Confirmation</DialogTitle>
      <DialogContent>
        <Stack>
          <Typography>{message}</Typography>
          <Button variant="contained" onClick={onConfirm}>
            Yes
          </Button>
          <Button variant="contained" onClick={onCancel}>
            No
          </Button>
        </Stack>
      </DialogContent>
    </Dialog>
  );
};

export { useConfirmation };
