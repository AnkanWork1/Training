import "./globals.css";
import Navbar from "../components/ui/Navbar";
import Sidebar from "../components/ui/Sidebar";

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-gray-100">
        {/* Top Navbar */}
        <Navbar />

        {/* Sidebar + Main Content */}
        <div className="flex">
          <Sidebar />

          <main className="ml-[260px] mt-16 p-8 w-full">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
