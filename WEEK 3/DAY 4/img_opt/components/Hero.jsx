import Image from "next/image";


export default function Hero() {
return (
<section className="max-w-7xl mx-auto px-6 py-20 grid md:grid-cols-2 gap-10 items-center">
<div>
<h1 className="text-4xl md:text-5xl font-bold leading-tight">
Build Faster with Purity UI
</h1>
<p className="mt-4 text-lg text-gray-600">
A modern SaaS dashboard & landing UI built with Next.js.
</p>
<button className="mt-6 bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition">
Get Started
</button>
</div>


<Image
src="/hero.png"
alt="Dashboard preview"
width={600}
height={400}
priority
className="w-full h-auto"
/>
</section>
);
}