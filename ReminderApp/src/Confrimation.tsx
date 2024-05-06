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
  confirmConfig?: ConfirmConfigProps;
  cancelConfig?: ConfirmConfigProps;
};

type ConfirmConfigProps = {
  text?: string;
  action?: () => void;
  [key: string]: any;
};

const defaultConfirmConfig = {
  text: "Confirm",
  action: () => {},
};

const defaultCancelConfig = {
  text: "Cancel",
  action: () => {},
  variant: "outlined",
};

const useConfirmation = ({
  message,
  confirmConfig = defaultConfirmConfig,
  cancelConfig = defaultCancelConfig,
}: useConfirmationProps) => {
  const [isOpen, setIsOpen] = useState(false);

  confirmConfig = { ...defaultConfirmConfig, ...confirmConfig };
  cancelConfig = { ...defaultCancelConfig, ...cancelConfig };

  const confirmation = (
    <Confirmation
      message={message}
      confirmConfig={confirmConfig}
      cancelConfig={cancelConfig}
      isOpen={isOpen}
      setIsOpen={setIsOpen}
    />
  );

  return { confirmation, showConfirmation: () => setIsOpen(true) };
};

type ConfirmationProps = {
  message: string;
  confirmConfig: ConfirmConfigProps;
  cancelConfig: ConfirmConfigProps;
  isOpen: boolean;
  setIsOpen: (isOpen: boolean) => void;
};

const Confirmation = ({
  message,
  isOpen,
  setIsOpen,
  confirmConfig,
  cancelConfig,
}: ConfirmationProps) => {
  const {
    text: confirmText,
    action: onConfirm,
    ...confirmButtonProps
  } = confirmConfig;
  const {
    text: cancelText,
    action: onCancel,
    ...cancelButtonProps
  } = cancelConfig;

  const handleConfirm = () => {
    setIsOpen(false);
    confirmConfig.action!();
  };

  const handleCancel = () => {
    setIsOpen(false);
    cancelConfig.action!();
  };

  return (
    <Dialog
      open={isOpen}
      onClose={() => setIsOpen(false)}
      fullWidth
      maxWidth="xs"
    >
      <DialogTitle>Confirmation</DialogTitle>
      <DialogContent>
        <Typography>{message}</Typography>
      </DialogContent>
      <DialogActions>
        <Button
          variant="contained"
          onClick={handleConfirm}
          {...confirmButtonProps}
        >
          {confirmText}
        </Button>
        <Button
          variant="contained"
          onClick={handleCancel}
          {...cancelButtonProps}
        >
          {cancelText}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export { useConfirmation };
