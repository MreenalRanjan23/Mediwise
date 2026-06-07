"use client";

import { motion } from "framer-motion";

import {
  ShieldCheck,
  AlertTriangle,
  Brain,
  Activity,
  Pill,
  HeartPulse,
} from "lucide-react";

const insights = [
  {
    title: "Medication Safety",
    message:
      "Paracetamol dosage appears clinically safe with no immediate toxicity concerns.",
    icon: ShieldCheck,
    glow: "from-emerald-500/20 to-green-500/5",
    border: "border-emerald-500/20",
    iconColor: "text-emerald-300",
  },

  {
    title: "Hydration Monitoring",
    message:
      "Increased hydration is recommended while taking Ibuprofen regularly.",
    icon: Activity,
    glow: "from-cyan-500/20 to-blue-500/5",
    border: "border-cyan-500/20",
    iconColor: "text-cyan-300",
  },

  {
    title: "Interaction Analysis",
    message:
      "No severe drug-drug interactions detected in the current medication plan.",
    icon: Brain,
    glow: "from-violet-500/20 to-purple-500/5",
    border: "border-violet-500/20",
    iconColor: "text-violet-300",
  },

  {
    title: "Toxicity Risk",
    message:
      "Liver toxicity probability is currently low based on dosage frequency.",
    icon: AlertTriangle,
    glow: "from-orange-500/20 to-red-500/5",
    border: "border-orange-500/20",
    iconColor: "text-orange-300",
  },

  {
    title: "Cardiovascular Status",
    message:
      "No cardiovascular overload indicators detected from active medications.",
    icon: HeartPulse,
    glow: "from-pink-500/20 to-rose-500/5",
    border: "border-pink-500/20",
    iconColor: "text-pink-300",
  },

  {
    title: "Medication Adherence",
    message:
      "Medication timing consistency appears stable and within safe intervals.",
    icon: Pill,
    glow: "from-blue-500/20 to-indigo-500/5",
    border: "border-blue-500/20",
    iconColor: "text-blue-300",
  },
];

export default function AIInsights() {

  return (

    <div className="space-y-6">

      {/* ================================================= */}
      {/* HEADER */}
      {/* ================================================= */}

      <div>

        <h2
          className="
            text-4xl
            font-black
            tracking-tight
            text-white
          "
        >
          AI Clinical Insights
        </h2>

        <p className="mt-3 text-gray-400 text-lg">
          Intelligent recommendations generated from medication analysis.
        </p>

      </div>

      {/* ================================================= */}
      {/* INSIGHTS GRID */}
      {/* ================================================= */}

      <div
        className="
          grid
          grid-cols-1
          xl:grid-cols-2
          gap-6
        "
      >

        {insights.map((item, index) => {

          const Icon = item.icon;

          return (

            <motion.div
              key={index}

              initial={{
                opacity: 0,
                y: 20,
              }}

              whileInView={{
                opacity: 1,
                y: 0,
              }}

              transition={{
                duration: 0.4,
                delay: index * 0.08,
              }}

              whileHover={{
                y: -4,
                scale: 1.01,
              }}

              className={`
                group
                relative
                overflow-hidden
                rounded-[28px]
                border
                ${item.border}
                bg-[#081120]/90
                p-6
                backdrop-blur-xl
                transition-all
                duration-300
              `}
            >

              {/* GLOW */}

              <div
                className={`
                  absolute
                  inset-0
                  bg-gradient-to-br
                  ${item.glow}
                  opacity-80
                `}
              />

              {/* LIGHT EFFECT */}

              <div
                className="
                  absolute
                  top-0
                  right-0
                  h-32
                  w-32
                  rounded-full
                  bg-white/5
                  blur-3xl
                "
              />

              {/* CONTENT */}

              <div className="relative z-10">

                {/* TOP */}

                <div className="flex items-start justify-between">

                  {/* ICON */}

                  <div
                    className="
                      flex
                      h-14
                      w-14
                      items-center
                      justify-center
                      rounded-2xl
                      border
                      border-white/10
                      bg-white/5
                      backdrop-blur-md
                    "
                  >

                    <Icon
                      className={`h-7 w-7 ${item.iconColor}`}
                    />

                  </div>

                  {/* STATUS DOT */}

                  <div
                    className="
                      h-3
                      w-3
                      rounded-full
                      bg-emerald-400
                      animate-pulse
                    "
                  />

                </div>

                {/* TEXT */}

                <div className="mt-6">

                  <h3
                    className="
                      text-2xl
                      font-bold
                      tracking-tight
                      text-white
                    "
                  >
                    {item.title}
                  </h3>

                  <p
                    className="
                      mt-3
                      text-gray-300
                      leading-relaxed
                      text-base
                    "
                  >
                    {item.message}
                  </p>

                </div>

              </div>

            </motion.div>

          );
        })}

      </div>

    </div>

  );
}