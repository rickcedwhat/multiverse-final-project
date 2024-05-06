import React from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Stack,
  LinearProgress,
  Typography,
} from "@mui/material";
import { SubmitHandler, useForm, Controller } from "react-hook-form";
import { DateTimeField } from "@mui/x-date-pickers";
import dayjs from "dayjs";
import { ReminderDB } from "../api";

type Inputs = {
  message: string;
  email: string;
  datetime: dayjs.Dayjs;
  phone: string;
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
  const {
    register,
    handleSubmit,
    control,
    formState: { errors },
  } = useForm({
    defaultValues: {
      message: initialReminder?.message || "",
      email: initialReminder?.email || "",
      datetime: dayjs(initialReminder?.datetime) || dayjs(),
      phone: initialReminder?.phone || "",
    },
  });

  const onSubmit: SubmitHandler<Inputs> = async (data) => {
    console.log(data);
    let response;
    // if initialReminder exists, edit the reminder
    if (initialReminder?.id) {
      console.log("Editing reminder");
      const updatedReminder = {
        message: data.message,
        email: data.email,
        datetime: data.datetime.toDate().toString(),
        phone: data.phone,
      };
      await mutations.edit.mutateAsync({
        reminder: updatedReminder,
        id: initialReminder.id,
      });
    } else {
      console.log("Creating reminder");
      const newReminder = {
        message: data.message,
        email: data.email,
        datetime: data.datetime.toDate().toString(),
        phone: data.phone,
      };
      await mutations.post.mutateAsync(newReminder);
    }
    handleClose();
  };

  const handleClose = () => {
    mutations.post.reset();
    mutations.edit.reset();
    onClose();
  };

  const mutationIsLoading =
    mutations.post.isLoading || mutations.edit.isLoading;
  const mutationError = mutations.post.isError || mutations.edit.isError;
  const mutationErrorMessage =
    mutations.post.error?.message + " " + mutations.edit.error?.message;

  return (
    <Dialog open={open} onClose={handleClose}>
      {mutationIsLoading && <LinearProgress />}
      <DialogTitle>
        {initialReminder?.id ? "Edit Reminder" : "Create Reminder"}
      </DialogTitle>
      <DialogContent>
        {mutationError && (
          <Typography variant="body1" color="error">
            {mutationErrorMessage}
          </Typography>
        )}
        <Stack spacing={2} direction="column" margin={2}>
          <TextField
            {...register("message", { required: "Message is required" })}
            label="Message"
            fullWidth
            helperText={errors.message?.message}
            error={!!errors.message}
          />
          <TextField
            {...register("email", {
              required: "Email is required",
              validate: (value) => {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                return emailRegex.test(value) || "Invalid email";
              },
            })}
            label="Email"
            fullWidth
            helperText={errors.email?.message}
            error={!!errors.email}
          />
          <Controller
            name="datetime"
            control={control}
            rules={{ required: "Datetime is required" }}
            render={({ field }) => (
              <DateTimeField
                {...field}
                label="Datetime"
                fullWidth
                slotProps={{
                  textField: {
                    helperText: errors.datetime?.message,
                    error: !!errors.datetime,
                  },
                }}
              />
            )}
          />
          <TextField
            {...register("phone", {
              required: "Phone is required",
              validate: (value) => {
                const phoneRegex = /^\d{10}$/;
                return phoneRegex.test(value) || "Invalid phone number";
              },
            })}
            label="Phone"
            fullWidth
            helperText={errors.phone?.message}
            error={!!errors.phone}
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
