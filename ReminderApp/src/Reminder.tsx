import React, { useState } from "react";
import { ReminderDB } from "../api";
import { Button, Card, CardContent, SxProps, Typography } from "@mui/material";

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
  };

  const sx: Record<string, unknown> = {};

  if (isSending) {
    sx.opacity = 0.5;
  }

  return (
    <Card sx={sx}>
      <CardContent>
        <Typography variant="h5" component="h2">
          {message}
        </Typography>
        <Typography color="textSecondary">{datetime.toString()}</Typography>
        <Typography color="textSecondary">{email}</Typography>
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
      </CardContent>
    </Card>
  );
};

export { Reminder };
