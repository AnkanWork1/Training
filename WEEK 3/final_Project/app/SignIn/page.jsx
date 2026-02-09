"use client";

import { useState } from "react";
import Modal from "../../components/Modal";
import Input from "../../components/Input";
import Button from "../../components/Button";

export default function SignInPage() {
  const [isModalOpen, setIsModalOpen] = useState(true);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Sign In"
      >
        <form className="flex flex-col gap-4">
          <Input type="email" placeholder="Email" />
          <Input type="password" placeholder="Password" />

          <Button type="submit" variant="solid">
            Sign In
          </Button>
        </form>

        <p className="text-sm text-gray-500 mt-4 text-center">
          Don&apos;t have an account?{" "}
          <a href="#" className="text-blue-600 hover:underline">
            Sign Up
          </a>
        </p>
      </Modal>
    </div>
  );
}
