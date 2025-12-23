// "use client" not needed here unless you use state/hooks
import Sidebar from "../../components/ui/Sidebar";

export default function UserProfile({ params }) {
  const { id } = params;

  // Mock user data
  const users = [
    { id: "1", name: "Alice", email: "alice@test.com", role: "Admin" },
    { id: "2", name: "Bob", email: "bob@test.com", role: "Editor" },
    { id: "3", name: "Charlie", email: "charlie@test.com", role: "Viewer" },
  ];

  const user = users.find((u) => u.id === id);

  if (!user) {
    return (
      <div className="flex">
        <Sidebar />
        <main className="ml-[260px] mt-16 p-8 w-full">User not found</main>
      </div>
    );
  }

  return (
    <div className="flex">
      <Sidebar />
      <main className="ml-[260px] mt-16 p-8 w-full">
        <h1 className="text-2xl font-bold mb-4">{user.name}</h1>
        <p>
          <strong>Email:</strong> {user.email}
        </p>
        <p>
          <strong>Role:</strong> {user.role}
        </p>
      </main>
    </div>
  );
}
