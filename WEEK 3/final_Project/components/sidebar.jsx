import Link from 'next/link';

export default function Sidebar() {
    return (
        <aside className=" w-62 bg-gray-100 h-[calc(100vh-56px)] pt-18 p-15">
      <nav className="flex flex-col gap-2">
        <Link href="/">Home</Link>
        <Link href="/dashboard">Dashboard</Link>
        <Link href="/Tables">Tables</Link>
        <Link href="../app/Signin">Sign in</Link>
      </nav>
    </aside>
    );
}