// pages/dashboard/users.js
import Navbar from "../../components/ui/Navbar";
import Sidebar from "../../components/ui/Sidebar";
import Table from "../../components/ui/Table";
import Badge from "../../components/ui/Badge";

export default function Users() {
  const columns = ["Author", "Function", "Status", "Employed", "Edit"];
  const data = [
    { author: "Esthera Jackson", function: "Manager", status: <Badge status="Online" />, employed: "14/06/21", edit: "Edit" },
    { author: "Alexa Liras", function: "Programmer", status: <Badge status="Offline" />, employed: "14/06/21", edit: "Edit" },
    { author: "Laurent Michael", function: "Executive", status: <Badge status="Online" />, employed: "14/06/21", edit: "Edit" },
  ];
  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1 min-h-screen bg-gray-100">
        <Navbar />
        <div className="p-6">
          <h1 className="text-2xl font-bold mb-4">Authors Table</h1>
          <Table columns={columns} data={data} />
        </div>
      </div>
    </div>
  );
}
