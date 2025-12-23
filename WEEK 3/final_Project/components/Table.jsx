"use client";

import { useState } from "react";
import Image from "next/image";
import Button from "../components/Button";
import Badge from "../components/Badge";
import Modal from "../components/Modal";

export default function Table({ users }) {
  const [selectedUser, setSelectedUser] = useState(null);

  return (
    <>
      <div className="overflow-x-auto bg-white shadow rounded-lg p-4 w-full">
        <h2 className="text-xl font-semibold mb-4">Authors Table</h2>
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-sm font-medium text-gray-500 uppercase tracking-wider">
                Author
              </th>
              <th className="px-6 py-3 text-left text-sm font-medium text-gray-500 uppercase tracking-wider">
                Function
              </th>
              <th className="px-6 py-3 text-left text-sm font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-3 text-left text-sm font-medium text-gray-500 uppercase tracking-wider">
                Employed
              </th>
              <th className="px-6 py-3 text-left text-sm font-medium text-gray-500 uppercase tracking-wider">
                Action
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {users.map((user, idx) => (
              <tr
                key={idx}
                className="cursor-pointer hover:bg-gray-50"
                onClick={() => setSelectedUser(user)}
              >
                {/* Author */}
                <td className="px-6 py-4 whitespace-nowrap flex items-center gap-3">
                  <Image
                    src={user.avatar}
                    alt={user.name}
                    width={40}
                    height={40}
                    className="rounded-full"
                  />
                  <div>
                    <div className="text-sm font-medium text-gray-900">{user.name}</div>
                    <div className="text-sm text-gray-500">{user.email}</div>
                  </div>
                </td>

                {/* Function */}
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-gray-900 font-medium">{user.role}</div>
                  <div className="text-sm text-gray-500">{user.department}</div>
                </td>

                {/* Status */}
                <td className="px-6 py-4 whitespace-nowrap">
                  <Badge color={user.status === "Online" ? "green" : "gray"}>
                    {user.status}
                  </Badge>
                </td>

                {/* Employed */}
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {user.employed}
                </td>

                {/* Action */}
                <td className="px-6 py-4 whitespace-nowrap">
                  <Button variant="outline" size="sm" onClick={(e) => e.stopPropagation()}>
                    Edit
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Modal */}
      <Modal isOpen={!!selectedUser} onClose={() => setSelectedUser(null)}>
        {selectedUser && (
          <div className="text-center">
            <Image
              src={selectedUser.avatar}
              alt={selectedUser.name}
              width={80}
              height={80}
              className="mx-auto rounded-full mb-4"
            />
            <h2 className="text-xl font-bold mb-2">{selectedUser.name}</h2>
            <p className="text-sm text-gray-500 mb-2">{selectedUser.email}</p>
            <p className="text-sm text-gray-700 mb-1"><strong>Role:</strong> {selectedUser.role}</p>
            <p className="text-sm text-gray-700 mb-1"><strong>Department:</strong> {selectedUser.department}</p>
            <p className="text-sm text-gray-700 mb-1"><strong>Status:</strong> {selectedUser.status}</p>
            <p className="text-sm text-gray-700"><strong>Employed:</strong> {selectedUser.employed}</p>
          </div>
        )}
      </Modal>
    </>
  );
}
