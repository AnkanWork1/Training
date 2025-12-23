import Card from "@/components/ui/Card";

const stats = [
  { title: "Users", value: "1,240" },
  { title: "Revenue", value: "$32k" },
  { title: "Orders", value: "320" },
  { title: "Growth", value: "+12%" },
];

export default function DashboardPage() {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      {stats.map((stat, i) => (
        <Card key={i}>
          <p className="text-sm text-gray-500">{stat.title}</p>
          <h3 className="text-2xl font-bold text-gray-800">
            {stat.value}
          </h3>
        </Card>
      ))}
    </div>
  );
}
