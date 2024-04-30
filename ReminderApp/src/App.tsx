import React from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { Reminders } from "./Reminders";

const queryClient = new QueryClient();

const App = () => {
  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <QueryClientProvider client={queryClient}>
        <Reminders />
      </QueryClientProvider>
    </LocalizationProvider>
  );
};

export default App;
