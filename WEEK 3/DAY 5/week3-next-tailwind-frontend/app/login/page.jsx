import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <Card className="w-full max-w-sm">
        <h2 className="text-xl font-semibold mb-6 text-center">
          Login
        </h2>

        <form className="space-y-4">
          <input
            type="email"
            placeholder="Email"
            className="w-full border rounded-lg px-4 py-2"
          />

          <input
            type="password"
            placeholder="Password"
            className="w-full border rounded-lg px-4 py-2"
          />

          <Button className="w-full">Sign In</Button>
        </form>
      </Card>
    </div>
  );
}
