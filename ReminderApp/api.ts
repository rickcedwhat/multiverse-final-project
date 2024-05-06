export interface ReminderDB {
  id: number;
  message: string;
  datetime: Date;
  email: string;
  phone: string;
}

export async function getReminders() {
  const response = await fetch("http://localhost:8000/reminders");
  const data = await response.json();
  return data;
}

export async function editReminder(id: number, reminder: Partial<ReminderDB>) {
  const response = await fetch(`http://localhost:8000/reminders/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(reminder),
  });
  const data = await response.json();
  return data;
}

export async function postReminder(reminder: Partial<ReminderDB>) {
  const response = await fetch("http://localhost:8000/reminders", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(reminder),
  });
  if (!response.ok) {
    // get error message
    throw new Error(response.statusText);
  }
  const data = await response.json();
  return data;
}

export async function deleteReminder(id: number) {
  const response = await fetch(`http://localhost:8000/reminders/${id}`, {
    method: "DELETE",
  });
  const data = await response.json();
  return data;
}

export async function deleteAllReminders() {
  const response = await fetch(`http://localhost:8000/reminders`, {
    method: "DELETE",
  });
  const data = await response.json();
  return data;
}
