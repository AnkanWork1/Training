export default function Badge({ text, color = "gray" }) {
  const colors = {
    gray: "bg-gray-100 text-gray-600",
    green: "bg-green-100 text-green-600",
    red: "bg-red-100 text-red-600",
    blue: "bg-blue-100 text-blue-600",
  };

  return (
    <span
      className={`px-2 py-1 rounded-full text-xs font-medium ${colors[color]}`}
    >
      {text}
    </span>
  );
}
