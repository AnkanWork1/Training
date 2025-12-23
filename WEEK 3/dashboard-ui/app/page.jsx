import Image from "next/image";

import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";

export const metadata = {
  title: "Purity UI | SaaS Landing",
  description: "Modern SaaS landing page built with Next.js & Tailwind",
};

export default function HomePage() {
  return (
    <main className="flex flex-col gap-24">

      {/* HERO SECTION */}
      <section className="flex flex-col-reverse lg:flex-row items-center justify-between px-8 py-16 max-w-7xl mx-auto">
        <div className="max-w-xl">
          <h1 className="text-4xl lg:text-5xl font-bold leading-tight">
            Build Faster with Purity UI
          </h1>
          <p className="text-gray-600 mt-4">
            Production-ready dashboard and UI components for modern SaaS products.
          </p>
          <div className="mt-6 flex gap-4">
            <Button>Get Started</Button>
            <Button variant="outline">Live Demo</Button>
          </div>
        </div>

        <Image
          src="/images/hero.png"
          alt="Dashboard Preview"
          width={500}
          height={400}
          className="mb-10 lg:mb-0"
          priority
        />
      </section>

      {/* FEATURES */}
      <section className="px-8 max-w-7xl mx-auto">
        <h2 className="text-3xl font-semibold text-center mb-12">
          Features
        </h2>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <Card>
            <h3 className="font-semibold mb-2">Next.js App Router</h3>
            <p className="text-gray-600">File-based routing with layouts</p>
          </Card>

          <Card>
            <h3 className="font-semibold mb-2">TailwindCSS</h3>
            <p className="text-gray-600">Utility-first & responsive UI</p>
          </Card>

          <Card>
            <h3 className="font-semibold mb-2">Reusable Components</h3>
            <p className="text-gray-600">Atomic design approach</p>
          </Card>
        </div>
      </section>

      {/* TESTIMONIALS */}
      <section className="bg-gray-50 py-16">
        <div className="max-w-7xl mx-auto px-8">
          <h2 className="text-3xl font-semibold text-center mb-12">
            What Users Say
          </h2>

          <div className="grid md:grid-cols-3 gap-6">
            <Card>
              <p>"This dashboard saved us weeks of work."</p>
              <span className="text-sm text-gray-500 mt-2 block">
                — Product Manager
              </span>
            </Card>

            <Card>
              <p>"Clean UI and great component structure."</p>
              <span className="text-sm text-gray-500 mt-2 block">
                — Frontend Developer
              </span>
            </Card>

            <Card>
              <p>"Perfect for SaaS MVPs."</p>
              <span className="text-sm text-gray-500 mt-2 block">
                — Startup Founder
              </span>
            </Card>
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="border-t py-6 text-center text-gray-500">
        © 2025 Purity UI. All rights reserved.
      </footer>

    </main>
  );
}
