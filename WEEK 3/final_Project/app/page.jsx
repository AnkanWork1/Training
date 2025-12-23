// app/page.jsx
import Image from 'next/image';
export default function HomePage() {
  const features = [
    { title: "Fast Performance", desc: "Our app runs lightning fast with optimized code." },
    { title: "Responsive Design", desc: "Looks great on any device, mobile or desktop." },
    { title: "Secure", desc: "We prioritize security with top-notch practices." },
    { title: "Customizable", desc: "Easily adapt features to your workflow." },
  ];

  const testimonials = [
    { name: "Alice Johnson", feedback: "This platform changed the way I work!", avatar: "/user1.png" },
    { name: "Bob Smith", feedback: "Amazing UI and very intuitive.", avatar: "/user2.png" },
    { name: "Carol White", feedback: "Excellent support and reliable service.", avatar: "/user2.png" },
  ];

  return (
    <div className="flex flex-col min-h-screen">
      {/* Hero Section with Image */}
      <section className="bg-blue-900 text-white py-20 px-6">
        <div className="max-w-6xl mx-auto flex flex-col-reverse md:flex-row items-center gap-10">
          {/* Text Content */}
          <div className="md:w-1/2 text-center md:text-left">
            <h1 className="text-4xl md:text-6xl font-bold mb-4">Welcome to Our Platform</h1>
            <p className="text-lg md:text-2xl mb-8">Build, launch, and scale your ideas effortlessly.</p>
            <button className="bg-white text-blue-600 font-semibold px-6 py-3 rounded hover:bg-gray-100 transition">
              Get Started
            </button>
          </div>

          {/* Hero Image */}
          <div className="md:w-1/2">
            <Image
              src="/people-image.png" // put your hero image in public/images
              alt="Hero Image"
              width={600}
              height={400}
              className="rounded-lg shadow-lg mx-auto"
            />
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-20 px-6 bg-gray-50">
        <h2 className="text-3xl font-bold text-center mb-12">Features</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 max-w-6xl mx-auto">
          {features.map((feature, idx) => (
            <div key={idx} className="bg-white p-6 rounded shadow hover:shadow-lg transition">
              <h3 className="font-semibold text-xl mb-2">{feature.title}</h3>
              <p className="text-gray-600">{feature.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-20 px-6 bg-white">
        <h2 className="text-3xl font-bold text-center mb-12">What Our Users Say</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {testimonials.map((t, idx) => (
            <div key={idx} className="bg-gray-50 p-6 rounded shadow text-center">
              <Image src={t.avatar} alt={t.name} width={80} height={80} className="rounded-full mx-auto mb-4"/>
              <p className="text-gray-700 italic mb-2">"{t.feedback}"</p>
              <p className="font-semibold">{t.name}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-10 px-6 mt-auto">
        <div className="max-w-6xl mx-auto text-center">
          <p>&copy; {new Date().getFullYear()} Your Company. All rights reserved.</p>
          <div className="mt-4 flex justify-center gap-4">
            <a href="#" className="hover:underline">Privacy Policy</a>
            <a href="#" className="hover:underline">Terms of Service</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
