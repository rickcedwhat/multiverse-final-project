import React, { useState } from "react";
import { Reminder } from "./Reminder";
import { Stack, Button, Typography, TextField, Grid } from "@mui/material";
import {
  useQuery,
  useMutation,
  useQueryClient,
  QueryClient,
  QueryClientProvider,
} from "@tanstack/react-query";
import {
  getReminders,
  postReminder,
  deleteReminder,
  editReminder,
  ReminderDB,
} from "../api.js";
import { ReminderPopup } from "./ReminderPopup";

const Reminders = () => {
  const queryClient = useQueryClient();
  const [currentReminder, setCurrentReminder] = useState<
    ReminderDB | Partial<ReminderDB> | null
  >(null);

  //   TODO: Add a form to add or edit a reminder

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
      queryClient.invalidateQueries({ queryKey: ["reminders"] });
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

  const newReminder: Partial<ReminderDB> = {
    message: "New Reminder",
    datetime: new Date(),
    email: "",
  };

  console.log({ currentReminder });

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
      <Button
        variant="contained"
        onClick={() => setCurrentReminder(newReminder)}
      >
        Add Reminder
      </Button>
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
