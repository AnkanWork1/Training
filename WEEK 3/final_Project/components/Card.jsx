export default function Card({ title, children }) {
  return (
    <div className="bg-white rounded-xl border shadow-sm">
      {title && (
        <div className="border-b px-6 py-4 text-sm font-semibold text-gray-700">
          {title}
        </div>
      )}

      <div className="p-6">
        {children}
      </div>
    </div>
  );
}
