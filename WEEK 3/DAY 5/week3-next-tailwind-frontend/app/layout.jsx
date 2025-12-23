// app/layout.jsx
import Navbar from "../components/ui/Navbar";
import Sidebar from "../components/ui/Sidebar";
import "../globals.css"; // Tailwind or global styles

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-gray-100">
        {/* Navbar */}
        <Navbar />

        <div className="flex">
          {/* Sidebar */}
          <Sidebar />

          {/* Main content */}
          <main className="ml-[260px] mt-16 p-8 w-full">{children}</main>
        </div>
      </body>
    </html>
  );
}
