import React from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Stack,
} from "@mui/material";
import { SubmitHandler, useForm, Controller } from "react-hook-form";
import { DateTimeField } from "@mui/x-date-pickers";
import dayjs from "dayjs";
import { ReminderDB } from "../api";

type Inputs = {
  message: string;
  email: string;
  datetime: dayjs.Dayjs;
};

type ReminderPopupProps = {
  open: boolean;
  onClose: () => void;
  initialReminder: ReminderDB | Partial<ReminderDB> | null;
  mutations: {
    post: any;
    edit: any;
  };
};

const ReminderPopup: React.FC<ReminderPopupProps> = ({
  open,
  onClose,
  initialReminder,
  mutations,
}) => {
  const { register, handleSubmit, control } = useForm({
    defaultValues: {
      message: initialReminder?.message || "",
      email: initialReminder?.email || "",
      datetime: dayjs(initialReminder?.datetime) || dayjs(),
    },
  });

  console.log({ initialReminder });

  const onSubmit: SubmitHandler<Inputs> = (data) => {
    console.log(data);
    // if initialReminder exists, edit the reminder
    if (initialReminder?.id) {
      console.log("Editing reminder");
      const updatedReminder = {
        message: data.message,
        email: data.email,
        datetime: data.datetime.toDate().toString(),
      };
      mutations.edit.mutateAsync({
        reminder: updatedReminder,
        id: initialReminder.id,
      });
    } else {
      console.log("Creating reminder");
      const newReminder = {
        message: data.message,
        email: data.email,
        datetime: data.datetime.toDate().toString(),
      };
      mutations.post.mutateAsync(newReminder);
    }
    onClose();
  };

  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>
        {initialReminder?.id ? "Edit Reminder" : "Create Reminder"}
      </DialogTitle>
      <DialogContent>
        <Stack spacing={2} direction="column" margin={2}>
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
          <Controller
            name="datetime"
            control={control}
            render={({ field }) => (
              <DateTimeField {...field} label="Datetime" fullWidth />
            )}
          />
        </Stack>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button onClick={handleSubmit(onSubmit)}>Submit</Button>
      </DialogActions>
    </Dialog>
  );
};

export { ReminderPopup };
