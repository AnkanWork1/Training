"use client";

import Table from "@/components/Table";
console.log(Table); // should be a function, not {}
console.log(12333333333333333333);

// Example user data
const users = [
  {
    name: "Esthera Jackson",
    email: "esthera@simmple.com",
    avatar: "/images/user1.jpg",
    role: "Manager",
    department: "Organization",
    status: "Online",
    employed: "14/06/21",
  },
  {
    name: "Alexa Liras",
    email: "alexa@simmple.com",
    avatar: "/images/user2.jpg",
    role: "Programmer",
    department: "Developer",
    status: "Offline",
    employed: "14/06/21",
  },
  {
    name: "Laurent Michael",
    email: "laurent@simmple.com",
    avatar: "/images/user3.jpg",
    role: "Executive",
    department: "Projects",
    status: "Online",
    employed: "14/06/21",
  },
  {
    name: "Freduardo Hill",
    email: "freduardo@simmple.com",
    avatar: "/images/user4.jpg",
    role: "Manager",
    department: "Organization",
    status: "Online",
    employed: "14/06/21",
  },
  {
    name: "Daniel Thomas",
    email: "daniel@simmple.com",
    avatar: "/images/user5.jpg",
    role: "Programmer",
    department: "Developer",
    status: "Offline",
    employed: "14/06/21",
  },
  {
    name: "Mark Wilson",
    email: "mark@simmple.com",
    avatar: "/images/user6.jpg",
    role: "Designer",
    department: "UI/UX Design",
    status: "Offline",
    employed: "14/06/21",
  },
];

export default function UsersPage() {
  return (
    <div className="p-6">
      <Table users={users} />
    </div>
  );
}
