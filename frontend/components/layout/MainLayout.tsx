"use client";

import Link from "next/link";

import {
  LayoutDashboard,
  Pill,
  BrainCircuit,
  FlaskConical,
  Bell,
  Sparkles,
  ChevronRight,
} from "lucide-react";

export default function MainLayout({
  children,
}: {
  children: React.ReactNode;
}) {

  const navItems = [
    {
      name: "Medication Planner",
      icon: Pill,
      active: true,
    },

    {
      name: "Dashboard",
      icon: LayoutDashboard,
    },

    {
      name: "AI Analysis",
      icon: BrainCircuit,
    },

    {
      name: "Simulation Lab",
      icon: FlaskConical,
    },

    {
      name: "Monitoring",
      icon: Bell,
    },
  ];

  return (

    <div className="min-h-screen bg-[#030712] text-white flex">

      {/* ================================================= */}
      {/* SIDEBAR */}
      {/* ================================================= */}

      <aside
        className="
          relative
          w-[290px]
          min-h-screen
          border-r
          border-white/10
          bg-gradient-to-b
          from-[#060816]
          via-[#040B1A]
          to-[#020611]
          px-6
          py-8
          flex
          flex-col
          justify-between
          overflow-hidden
        "
      >

        {/* glow */}
        <div
          className="
            absolute
            top-[-120px]
            left-[-120px]
            h-[260px]
            w-[260px]
            rounded-full
            bg-blue-500/10
            blur-[100px]
            pointer-events-none
          "
        />

        {/* ================================================= */}
        {/* TOP SECTION */}
        {/* ================================================= */}

        <div className="relative z-10">

          {/* LOGO */}
          <div className="mb-12">

            <div className="flex items-center gap-3">

              <div
                className="
                  h-11
                  w-11
                  rounded-2xl
                  bg-gradient-to-br
                  from-blue-500
                  to-purple-600
                  flex
                  items-center
                  justify-center
                  shadow-lg
                  shadow-blue-500/30
                "
              >
                <Sparkles className="w-5 h-5 text-white" />
              </div>

              <div>

                <h1
                  className="
                    text-4xl
                    font-black
                    tracking-tight
                    leading-none
                  "
                >
                  <span className="text-white">
                    Medi
                  </span>

                  <span
                    className="
                      bg-gradient-to-r
                      from-blue-400
                      to-purple-500
                      bg-clip-text
                      text-transparent
                    "
                  >
                    Wise
                  </span>
                </h1>

                <p className="text-gray-500 text-sm mt-1">
                  Clinical Intelligence
                </p>

              </div>

            </div>

          </div>

          {/* SECTION LABEL */}
          <div className="mb-4 px-3">

            <p
              className="
                text-xs
                uppercase
                tracking-[0.2em]
                text-gray-500
                font-semibold
              "
            >
              Workspace
            </p>

          </div>

          {/* ================================================= */}
          {/* NAVIGATION */}
          {/* ================================================= */}

          <nav className="space-y-3">

            {navItems.map((item, index) => {

              const Icon = item.icon;

              return (

                <Link
                  key={index}
                  href="#"
                  className={`
                    group
                    relative
                    flex
                    items-center
                    justify-between
                    rounded-2xl
                    px-4
                    py-4
                    transition-all
                    duration-300

                    ${
                      item.active
                        ? `
                          bg-gradient-to-r
                          from-blue-500/20
                          to-purple-500/20
                          border
                          border-blue-500/20
                          shadow-lg
                          shadow-blue-500/10
                        `
                        : `
                          border
                          border-transparent
                          hover:border-white/10
                          hover:bg-white/[0.03]
                        `
                    }
                  `}
                >

                  {/* LEFT */}
                  <div className="flex items-center gap-4">

                    {/* ICON BOX */}
                    <div
                      className={`
                        h-11
                        w-11
                        rounded-xl
                        flex
                        items-center
                        justify-center
                        border
                        transition-all
                        duration-300

                        ${
                          item.active
                            ? `
                              border-blue-400/20
                              bg-blue-500/10
                              text-blue-300
                            `
                            : `
                              border-white/5
                              bg-white/[0.03]
                              text-gray-400
                              group-hover:text-white
                            `
                        }
                      `}
                    >

                      <Icon className="w-5 h-5" />

                    </div>

                    {/* TEXT */}
                    <div>

                      <p
                        className={`
                          text-lg
                          font-medium
                          transition-colors

                          ${
                            item.active
                              ? "text-white"
                              : "text-gray-300 group-hover:text-white"
                          }
                        `}
                      >
                        {item.name}
                      </p>

                      <p className="text-xs text-gray-500 mt-0.5">
                        {
                          index === 0
                            ? "Medication management"
                            : index === 1
                            ? "System overview"
                            : index === 2
                            ? "Clinical intelligence"
                            : index === 3
                            ? "Counterfactual testing"
                            : "Real-time alerts"
                        }
                      </p>

                    </div>

                  </div>

                  {/* RIGHT ARROW */}
                  <ChevronRight
                    className="
                      w-4
                      h-4
                      text-gray-600
                      opacity-0
                      group-hover:opacity-100
                      transition-all
                      duration-300
                      group-hover:translate-x-1
                    "
                  />

                </Link>
              );
            })}

          </nav>

        </div>

        {/* ================================================= */}
        {/* BOTTOM AI CARD */}
        {/* ================================================= */}

        <div className="relative z-10">

          <div
            className="
              relative
              overflow-hidden
              rounded-3xl
              border
              border-white/10
              bg-gradient-to-br
              from-[#111827]
              via-[#0E1729]
              to-[#111827]
              p-6
            "
          >

            {/* glow */}
            <div
              className="
                absolute
                top-[-40px]
                right-[-40px]
                h-28
                w-28
                rounded-full
                bg-purple-500/20
                blur-3xl
              "
            />

            <div className="relative z-10">

              <div
                className="
                  h-12
                  w-12
                  rounded-2xl
                  bg-gradient-to-br
                  from-blue-500
                  to-purple-600
                  flex
                  items-center
                  justify-center
                  shadow-lg
                  shadow-blue-500/20
                "
              >
                <BrainCircuit className="w-6 h-6 text-white" />
              </div>

              <h3 className="mt-5 text-lg font-semibold">
                AI Health Assistant
              </h3>

              <p className="text-gray-400 text-sm mt-2 leading-relaxed">
                Intelligent medication safety monitoring
                with real-time clinical insights.
              </p>

              <button
                className="
                  mt-5
                  w-full
                  rounded-xl
                  border
                  border-white/10
                  bg-white/5
                  py-3
                  text-sm
                  font-medium
                  text-white
                  transition-all
                  duration-300
                  hover:bg-white/10
                "
              >
                Open Assistant
              </button>

            </div>

          </div>

        </div>

      </aside>

      {/* ================================================= */}
      {/* MAIN CONTENT */}
      {/* ================================================= */}

      <main className="flex-1 overflow-y-auto">
        {children}
      </main>

    </div>
  );
}