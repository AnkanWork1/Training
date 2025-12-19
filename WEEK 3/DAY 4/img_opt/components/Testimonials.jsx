import Image from "next/image";


const users = [
{ name: "Alex", img: "/user1.png", text: "Amazing UI & performance." },
{ name: "Sam", img: "/user2.png", text: "Perfect for SaaS projects." },
];


export default function Testimonials() {
return (
<section className="py-20 bg-gray-100">
<div className="max-w-6xl mx-auto px-6">
<h2 className="text-3xl font-bold text-center">Testimonials</h2>


<div className="mt-12 grid gap-8 md:grid-cols-2">
{users.map((u, i) => (
<div key={i} className="bg-white p-6 rounded-lg shadow">
<Image
src={u.img}
alt={u.name}
width={50}
height={50}
className="rounded-full"
/>
<p className="mt-4 text-gray-600">"{u.text}"</p>
<p className="mt-2 font-semibold">– {u.name}</p>
</div>
))}
</div>
</div>
</section>
);
}