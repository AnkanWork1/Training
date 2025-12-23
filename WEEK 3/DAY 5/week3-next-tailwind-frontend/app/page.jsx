// pages/dashboard/index.js
import Navbar from "../components/ui/Navbar";
import Sidebar from "../components/ui/Sidebar";
import Card from "../components/ui/Card";
import { UsersIcon, CurrencyDollarIcon } from "@heroicons/react/outline";
import Image from "next/image";

export default function Dashboard() {
  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1 min-h-screen bg-gray-100">
        <Navbar />
        <div className="p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card title="Today's Money" value="$53,000" icon={<CurrencyDollarIcon className="h-6 w-6" />} footer="+55%" />
          <Card title="Today's Users" value="2,300" icon={<UsersIcon className="h-6 w-6" />} footer="+5%" />
          <Card title="New Clients" value="+3,052" icon={<UsersIcon className="h-6 w-6" />} footer="-14%" />
          <Card title="Total Sales" value="$173,000" icon={<CurrencyDollarIcon className="h-6 w-6" />} footer="+8%" />
        </div>

        <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-white rounded shadow p-4">
            <Image src="/images/dashboard-banner.jpg" width={500} height={200} alt="Banner" />
          </div>
          <div className="bg-white rounded shadow p-4">
            <p>Work with the Rockets - Wealth creation is an evolutionary recent positive-sum game...</p>
          </div>
        </div>
      </div>
    </div>
  );
}
