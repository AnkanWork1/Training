import Image from "next/image";


const features = [
{ title: "Fast Performance", img: "/feature1.png" },
{ title: "Responsive UI", img: "/feature2.png" },
{ title: "SEO Optimized", img: "/feature3.png" },
];


export default function Features() {
return (
<section className="bg-white py-20">
<div className="max-w-7xl mx-auto px-6">
<h2 className="text-3xl font-bold text-center">Features</h2>


<div className="mt-12 grid gap-8 sm:grid-cols-2 md:grid-cols-3">
{features.map((f, i) => (
<div
key={i}
className="p-6 border rounded-lg hover:shadow-lg transition"
>
<Image
src={f.img}
alt={f.title}
width={200}
height={120}
className="mx-auto"
/>
<h3 className="mt-4 text-xl font-semibold text-center">
{f.title}
</h3>
</div>
))}
</div>
</div>
</section>
);
}