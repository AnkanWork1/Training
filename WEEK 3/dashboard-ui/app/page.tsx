import Link from "next/link";

export default function Home() {
  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">
        Dashboard Overview
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          Card 1
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          Card 2
        </div>
      </div>

      <Link href="/about">
        Go to About Page
      </Link>
    </div>
  );
}
