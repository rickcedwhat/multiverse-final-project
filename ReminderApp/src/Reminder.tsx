import React, { useState } from "react";
import { ReminderDB } from "../api";
import { Button, Card, CardContent, Typography, Stack } from "@mui/material";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import { useConfirmation } from "./Confrimation";

dayjs.extend(relativeTime);

interface ReminderProps {
  reminder: ReminderDB;
  onDelete: (id: number) => Promise<void>;
  openPopup: (reminder: ReminderDB) => void;
}

const Reminder: React.FC<ReminderProps> = ({
  reminder,
  onDelete,
  openPopup,
}) => {
  const { id, message, datetime, email, phone } = reminder;

  const handleDelete = async () => {
    setIsSending(true);
    await onDelete(id);
    setIsSending(false);
  };

  const { confirmation, showConfirmation } = useConfirmation({
    message: "Are you sure you want to delete this reminder?",
    confirmConfig: {
      text: "Confirm Deletion",
      color: "error",
      action: handleDelete,
    },
  });

  const [isSending, setIsSending] = useState(false);

  const sx: Record<string, unknown> = {
    margin: "1rem",
    border: "1px solid black",
  };

  if (isSending) {
    sx.opacity = 0.5;
  }

  console.log({ datetime, dayjs });

  return (
    <Card sx={sx}>
      <CardContent>
        <Typography variant="caption">{id}</Typography>
        <Typography variant="h5">{message}</Typography>
        <Typography color="textSecondary">
          {dayjs(datetime).format("ddd MMM Do h:mm A")}
        </Typography>
        <Typography color="textSecondary">
          {dayjs(datetime).fromNow()}
        </Typography>
        <Typography color="textSecondary">{email}</Typography>
        <Typography color="textSecondary">{phone}</Typography>
        <Stack spacing={2} direction="row">
          <Button variant="contained" color="error" onClick={showConfirmation}>
            Delete
          </Button>
          <Button
            variant="contained"
            color="primary"
            onClick={() => openPopup(reminder)}
          >
            Edit
          </Button>
          {confirmation}
        </Stack>
      </CardContent>
    </Card>
  );
};

export { Reminder };
