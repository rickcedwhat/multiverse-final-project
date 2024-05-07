import React, { useState } from "react";
import { Reminder } from "./Reminder";
import { Stack, Button, Typography, TextField, Grid } from "@mui/material";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  getReminders,
  postReminder,
  deleteReminder,
  editReminder,
  deleteAllReminders,
  ReminderDB,
} from "../api.js";
import { ReminderPopup } from "./ReminderPopup";
import { useConfirmation } from "./Confrimation";

const Reminders = () => {
  const queryClient = useQueryClient();
  const [currentReminder, setCurrentReminder] = useState<
    ReminderDB | Partial<ReminderDB> | null
  >(null);

  const { confirmation, showConfirmation } = useConfirmation({
    message: "Are you sure you want to delete all reminders?",
    confirmConfig: {
      text: "Confirm Deletion",
      action: deleteAllReminders,
      variant: "contained",
      color: "error",
    },
    cancelConfig: { variant: "outlined" },
  });

  // Queries
  const {
    isPending,
    isError,
    data: reminders,
    error,
  } = useQuery<ReminderDB[]>({
    queryKey: ["reminders"],
    queryFn: getReminders,
  });

  // Mutations
  const postMutation = useMutation({
    mutationFn: postReminder,
    onSuccess: () => {
      // Invalidate and refetch
      console.log("Success");
      queryClient.invalidateQueries({ queryKey: ["reminders"] });
    },
    onError: (error) => {
      console.error("error", { error });
    },
  });

  const editMutation = useMutation({
    mutationFn: async ({
      reminder,
      id,
    }: {
      reminder: ReminderDB;
      id: number;
    }) => {
      await editReminder(id, reminder);
    },
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({ queryKey: ["reminders"] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: deleteReminder,
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({ queryKey: ["reminders"] });
    },
  });

  const handleDelete = async (id: number) => {
    await deleteMutation.mutateAsync(id);
  };

  const createNewReminder = () => {
    const newReminder: Partial<ReminderDB> = {
      message: "New Reminder",
      datetime: new Date(Date.now() + 60 * 60 * 1000),
      email: "ccata002@gmail.com",
      phone: "7864400382",
    };
    setCurrentReminder(newReminder);
  };

  return (
    <>
      <h1>Hello, React!</h1>
      {isPending && <p>Loading...</p>}
      {isError && <p>Error: {String(error)}</p>}
      <Grid container spacing={2} flexDirection="row" margin={2} gap={2}>
        {reminders?.map((reminder) => (
          <Reminder
            key={reminder.id}
            reminder={reminder}
            onDelete={handleDelete}
            openPopup={() => setCurrentReminder(reminder)}
          />
        ))}
      </Grid>
      <Button variant="contained" onClick={createNewReminder}>
        Add Reminder
      </Button>
      <Button variant="contained" onClick={showConfirmation}>
        Delete All
      </Button>
      {confirmation}
      {currentReminder && (
        <ReminderPopup
          open={true}
          onClose={() => setCurrentReminder(null)}
          mutations={{ post: postMutation, edit: editMutation }}
          initialReminder={currentReminder}
        />
      )}
    </>
  );
};

export { Reminders };
