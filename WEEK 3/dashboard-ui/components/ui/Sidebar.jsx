export default function Sidebar() {
  return (
    <aside className="fixed top-16 left-0 w-[260px] h-[calc(100vh-4rem)] px-6 py-8">
      
      <div className="bg-white rounded-xl shadow-sm h-full p-6">
        {/* Main Navigation */}
        <ul className="space-y-4 text-sm font-medium text-gray-700">
          <li className="flex items-center gap-2 px-3 py-2 rounded-lg bg-blue-50 text-blue-600">
            Dashboard
          </li>
          <li className="px-3 py-2 hover:text-blue-600 cursor-pointer">
            Tables
          </li>
          <li className="px-3 py-2 hover:text-blue-600 cursor-pointer">
            Billing
          </li>
          <li className="px-3 py-2 hover:text-blue-600 cursor-pointer">
            RTL
          </li>
        </ul>

        {/* Divider */}
        <div className="mt-8 mb-4 text-xs text-gray-400 uppercase">
          Account Pages
        </div>

        <ul className="space-y-3 text-sm text-gray-700">
          <li className="px-3 py-2 hover:text-blue-600 cursor-pointer">
            Profile
          </li>
          <li className="px-3 py-2 hover:text-blue-600 cursor-pointer">
            Sign In
          </li>
          <li className="px-3 py-2 hover:text-blue-600 cursor-pointer">
            Sign Up
          </li>
        </ul>
      </div>
    </aside>
  );
}
