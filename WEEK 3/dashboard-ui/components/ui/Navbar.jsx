export default function Navbar() {
  return (
    <header className="fixed top-0 left-0 right-0 h-16 bg-white border-b flex items-center justify-between px-8 z-50">
      {/* Left */}
      <div className="text-sm font-semibold text-gray-800">
        Purity UI Dashboard
      </div>

      {/* Right */}
      <div className="flex items-center gap-4">
        <input
          type="text"
          placeholder="Type here..."
          className="text-sm px-3 py-1.5 border rounded-md outline-none focus:ring-2 focus:ring-blue-500"
        />
        <span className="text-sm text-gray-600 cursor-pointer">
          Sign In
        </span>
      </div>
    </header>
  );
}
