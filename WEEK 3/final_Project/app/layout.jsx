import "../style/global.css";
import Navbar from "../components/navbar";
import Sidebar from "../components/sidebar";

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-gray-100">
        {/* Navbar */}
        <Navbar />

        {/* Sidebar + Content */}
        <div className="flex">
          <Sidebar />

          <main className="ml-[26px] mt-16 p-6">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
