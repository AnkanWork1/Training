import Card from "@/components/ui/Card";

export default function ProfilePage() {
  return (
    <div className="max-w-xl">
      <Card>
        <h2 className="text-lg font-semibold mb-4">Profile Information</h2>

        <div className="space-y-2 text-sm">
          <p><span className="text-gray-500">Name:</span> John Doe</p>
          <p><span className="text-gray-500">Email:</span> john@mail.com</p>
          <p><span className="text-gray-500">Role:</span> Admin</p>
        </div>
      </Card>
    </div>
  );
}
