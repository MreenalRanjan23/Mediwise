"use client";

import Link from "next/link";

export default function Sidebar() {
  return (
    <div className="w-64 h-screen bg-[#0B0F1A] text-white p-6">
      <h1 className="text-xl font-bold mb-8 text-blue-400">
        MediWise
      </h1>

      <ul className="space-y-4 text-gray-300">

        <li>
          <Link href="/" className="hover:text-white">Dashboard</Link>
        </li>

        <li>
          <Link href="/planner" className="hover:text-white">
            Medication Planner
          </Link>
        </li>

        <li>
          <Link href="/analysis" className="hover:text-white">
            Analysis
          </Link>
        </li>

        <li>
          <Link href="/simulation" className="hover:text-white">
            Simulation Lab
          </Link>
        </li>

        <li>
          <Link href="/monitoring" className="hover:text-white">
            Monitoring
          </Link>
        </li>

      </ul>

      <div className="absolute bottom-4 text-sm text-gray-500">
        © MediWise
      </div>
    </div>
  );
}