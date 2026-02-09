"use client";

import { useEffect, useState } from "react";

export default function DashboardPage() {
  const [stats, setStats] = useState({
    users: 0,
    revenue: 0,
    orders: 0,
    active: 0,
  });

  useEffect(() => {
    // fake API simulation (replace later with real API)
    setTimeout(() => {
      setStats({
        users: 1248,
        revenue: 58240,
        orders: 312,
        active: 87,
      });
    }, 400);
  }, []);

  return (
    <main className="p-6 bg-gray-50 min-h-screen">

      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-gray-800">
          Dashboard
        </h1>
        <p className="text-sm text-gray-500">
          Overview of your platform performance
        </p>
      </div>

      {/* KPI cards */}
      <section className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-6 mb-10">
        <StatCard title="Total Users" value={stats.users} />
        <StatCard title="Orders" value={stats.orders} />
        <StatCard title="Revenue" value={`$${stats.revenue}`} />
        <StatCard title="Active Sessions" value={stats.active} />
      </section>

      {/* Main content */}
      <section className="grid grid-cols-1 xl:grid-cols-3 gap-6">

        {/* Activity / chart placeholder */}
        <div className="xl:col-span-2 bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">
            Weekly activity
          </h2>

          <div className="h-64 flex items-center justify-center text-gray-400 border border-dashed rounded">
            Chart placeholder
          </div>
        </div>

        {/* Recent activity */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">
            Recent activity
          </h2>

          <ul className="space-y-4">
            <ActivityItem
              title="New user registered"
              subtitle="john@example.com"
            />
            <ActivityItem
              title="Order completed"
              subtitle="Order #18231"
            />
            <ActivityItem
              title="Payment received"
              subtitle="$240.00"
            />
            <ActivityItem
              title="New support ticket"
              subtitle="Login issue"
            />
          </ul>
        </div>
      </section>

      {/* Table */}
      <section className="mt-10 bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">
          Latest orders
        </h2>

        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="text-left text-gray-500 border-b">
              <tr>
                <th className="py-2">Order ID</th>
                <th className="py-2">Customer</th>
                <th className="py-2">Status</th>
                <th className="py-2">Amount</th>
              </tr>
            </thead>

            <tbody className="divide-y">
              <OrderRow
                id="#10231"
                customer="Alice Johnson"
                status="Completed"
                amount="$320"
              />
              <OrderRow
                id="#10232"
                customer="Bob Smith"
                status="Pending"
                amount="$120"
              />
              <OrderRow
                id="#10233"
                customer="Carol White"
                status="Completed"
                amount="$560"
              />
              <OrderRow
                id="#10234"
                customer="David Lee"
                status="Failed"
                amount="$90"
              />
            </tbody>
          </table>
        </div>
      </section>
    </main>
  );
}

/* ---------------- small components ---------------- */

function StatCard({ title, value }) {
  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <p className="text-sm text-gray-500">{title}</p>
      <p className="mt-2 text-2xl font-semibold text-gray-800">
        {value}
      </p>
    </div>
  );
}

function ActivityItem({ title, subtitle }) {
  return (
    <li className="flex items-start gap-3">
      <span className="mt-1 h-2 w-2 rounded-full bg-blue-600"></span>

      <div>
        <p className="text-sm font-medium text-gray-700">
          {title}
        </p>
        <p className="text-xs text-gray-500">
          {subtitle}
        </p>
      </div>
    </li>
  );
}

function OrderRow({ id, customer, status, amount }) {
  const color =
    status === "Completed"
      ? "text-green-600"
      : status === "Pending"
      ? "text-yellow-600"
      : "text-red-600";

  return (
    <tr>
      <td className="py-3">{id}</td>
      <td className="py-3">{customer}</td>
      <td className={`py-3 font-medium ${color}`}>
        {status}
      </td>
      <td className="py-3">{amount}</td>
    </tr>
  );
}
