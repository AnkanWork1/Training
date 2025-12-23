"use client";

import { useState } from "react";
import Modal from "../components/Modal";
import Input from "../components/Input";
import Button from "../components/Button";
import { usePathname } from "next/navigation";

export default function Navbar() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const pathname = usePathname();

  let title = "Home";
  if (pathname.startsWith("/dashboard")) title = "Dashboard";
  else if (pathname.startsWith("/table")) title = "Table";
  else if (pathname.startsWith("/login")) title = "Login";

  return (
    <>
      <header className="fixed top-0 left-0 right-0 h-16 bg-white shadow z-50">
        <div className="flex items-center justify-between h-full px-6">
          {/* Dynamic Heading */}
          <h1 className="text-xl font-semibold text-gray-800">{title}</h1>

          {/* Search Input */}
          <div className="hidden md:block w-[320px]">
            <Input type="text" placeholder="Search..." />
          </div>

          {/* Sign In Button */}
          <Button onClick={() => setIsModalOpen(true)} variant="outline">
            Sign In
          </Button>
        </div>
      </header>
      <h1>sdwafa</h1>

      {/* Sign-In Modal */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Sign In">
        <form className="flex flex-col gap-4">
          <Input type="email" placeholder="Email" />
          <Input type="password" placeholder="Password" />
          <Button type="submit" variant="solid">
            Sign In
          </Button>
        </form>
        <p className="text-sm text-gray-500 mt-4 text-center">
          Don't have an account?{" "}
          <a href="#" className="text-blue-600 hover:underline">
            Sign Up
          </a>
        </p>
      </Modal>
    </>
  );
}
