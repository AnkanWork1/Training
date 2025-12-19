export default function Footer() {
return (
<footer className="bg-gray-900 text-gray-300 py-10">
<div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between">
<p>© 2025 Purity UI</p>
<div className="flex gap-4 mt-4 md:mt-0">
<span className="cursor-pointer">Privacy</span>
<span className="cursor-pointer">Terms</span>
<span className="cursor-pointer">Contact</span>
</div>
</div>
</footer>
);
}