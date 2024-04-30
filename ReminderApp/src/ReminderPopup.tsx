import React, { useState } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
} from "@mui/material";
import { SubmitHandler, useForm } from "react-hook-form";
import { ReminderDB } from "../api";

type Inputs = {
  message: string;
  email: string;
};

type ReminderPopupProps = {
  open: boolean;
  onClose: () => void;
  initialReminder: ReminderDB | Partial<ReminderDB> | null;
  postMutation: any;
};

const ReminderPopup: React.FC<ReminderPopupProps> = ({
  open,
  onClose,
  initialReminder,
  postMutation,
}) => {
  const { register, handleSubmit } = useForm({
    defaultValues: {
      message: initialReminder?.message || "",
      email: initialReminder?.email || "",
    },
  });

  console.log({ initialReminder });

  const onSubmit: SubmitHandler<Inputs> = (data) => {
    console.log(data);
    // if initialReminder exists, edit the reminder
    if (initialReminder) {
      console.log("Editing reminder");
      // editReminder(initialReminder.id, data);
    } else {
      console.log("Creating reminder");
      const newReminder = {
        message: data.message,
        email: data.email,
        datetime: new Date(),
      };
      postMutation.mutateAsync(newReminder);
    }
    onClose();
  };

  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>
        {initialReminder ? "Edit Reminder" : "Create Reminder"}
      </DialogTitle>
      <DialogContent>
        <TextField
          {...register("message", { required: true })}
          label="Message"
          fullWidth
        />
        <TextField
          {...register("email", { required: true })}
          label="Email"
          fullWidth
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button onClick={handleSubmit(onSubmit)}>Submit</Button>
      </DialogActions>
    </Dialog>
  );
};

export { ReminderPopup };
