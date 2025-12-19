import Navbar from "@/components/Navbar";
import Sidebar from "@/components/Sidebar";

export default function DashboardLayout({ children }) {
  return (
    <div>
      <Navbar />

      <div className="flex">
        <Sidebar />
        <main className="ml-[260px] mt-16 p-8 w-full">
          {children}
        </main>
      </div>
    </div>
  );
}
