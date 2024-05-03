import React, { useState } from "react";
import { ReminderDB } from "../api";
import { Button, Card, CardContent, Typography, Stack } from "@mui/material";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";

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
  const { id, message, datetime, email } = reminder;
  const [isSending, setIsSending] = useState(false);

  const handleDelete = async () => {
    setIsSending(true);
    await onDelete(id);
    setIsSending(false);
  };

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
        <Typography variant="h5" component="h2">
          {message}
        </Typography>
        <Typography color="textSecondary">
          {dayjs(datetime).format("ddd MMM Do h:mm A")}
        </Typography>
        <Typography color="textSecondary">
          {dayjs(datetime).fromNow()}
        </Typography>
        <Typography color="textSecondary">{email}</Typography>
        <Stack spacing={2} direction="row">
          <Button variant="contained" color="error" onClick={handleDelete}>
            Delete
          </Button>
          <Button
            variant="contained"
            color="primary"
            onClick={() => openPopup(reminder)}
          >
            Edit
          </Button>
        </Stack>
      </CardContent>
    </Card>
  );
};

export { Reminder };
