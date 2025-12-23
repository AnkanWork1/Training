"use client";

import Table from "../../components/ui/Table";
import { useRouter } from "next/navigation";
import Sidebar from "../../components/ui/Sidebar";

export default function UsersList() {
  const router = useRouter();

  const users = [
    { id: 1, name: "Alice", email: "alice@test.com" },
    { id: 2, name: "Bob", email: "bob@test.com" },
    { id: 3, name: "Charlie", email: "charlie@test.com" },
  ];

  const columns = ["ID", "Name", "Email"];

  const handleRowClick = (user) => {
    router.push(`/tables/${user.id}`);
  };

  return (
    <div className="flex">
      <Sidebar />
      <main className="ml-[260px] mt-16 p-8 w-full">
        <h1 className="text-2xl font-bold mb-6">Users</h1>
        <Table columns={columns} data={users} onRowClick={handleRowClick} />
      </main>
    </div>
  );
}
