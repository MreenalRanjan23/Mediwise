"use client";

import {
  Pill,
  ShieldAlert,
  Activity,
  BrainCircuit,
} from "lucide-react";

interface TopStatsProps {
  drugs: any[];
  riskData: any;
}

export default function TopStats({
  drugs,
  riskData,
}: TopStatsProps) {

  const riskScore =
    riskData?.risk_analysis?.score ?? 0;

  const interactions =
    riskData?.risk_analysis?.interactions?.length ?? 0;

  const cardClass = `
    relative
    overflow-hidden
    rounded-[28px]
    border
    border-white/10
    p-6
    transition-all
    duration-300
    hover:-translate-y-1
    min-h-[220px]
  `;

  return (

    <div
      className="
        w-full
        grid
        grid-cols-1
        sm:grid-cols-2
        xl:grid-cols-4
        gap-6
      "
    >

      {/* ================================================= */}
      {/* ACTIVE MEDICATIONS */}
      {/* ================================================= */}

      <div
        className={`
          ${cardClass}
          bg-gradient-to-br
          from-slate-800/80
          to-blue-900/40
          hover:shadow-[0_0_35px_rgba(59,130,246,0.15)]
        `}
      >

        <div className="flex items-start justify-between">

          <div className="min-w-0">

            <p
              className="
                text-[11px]
                uppercase
                tracking-[0.35em]
                text-gray-400
              "
            >
              Active Medications
            </p>

            <h2
              className="
                mt-8
                text-6xl
                font-black
                leading-none
                text-white
              "
            >
              {drugs.length}
            </h2>

          </div>

          <div
            className="
              shrink-0
              rounded-[24px]
              border
              border-white/10
              bg-white/5
              p-4
            "
          >
            <Pill
              size={34}
              className="text-blue-300"
            />
          </div>

        </div>

        <p
          className="
            mt-10
            text-base
            text-gray-400
          "
        >
          Currently monitored
        </p>

      </div>

      {/* ================================================= */}
      {/* RISK SCORE */}
      {/* ================================================= */}

      <div
        className={`
          ${cardClass}
          bg-gradient-to-br
          from-emerald-900/30
          to-cyan-900/30
          hover:shadow-[0_0_35px_rgba(16,185,129,0.18)]
        `}
      >

        <div className="flex items-start justify-between gap-4">

          <div className="min-w-0 flex-1">

            <p
              className="
                text-[11px]
                uppercase
                tracking-[0.35em]
                text-gray-400
              "
            >
              Risk Score
            </p>

            <h2
              className="
                mt-8
                text-5xl
                font-black
                leading-none
                text-white
                whitespace-nowrap
              "
            >
              {Number(riskScore).toFixed(2)}
            </h2>

          </div>

          <div
            className="
              shrink-0
              rounded-[24px]
              border
              border-white/10
              bg-white/5
              p-4
            "
          >
            <ShieldAlert
              size={34}
              className="text-emerald-300"
            />
          </div>

        </div>

        <p
          className="
            mt-10
            text-base
            text-gray-400
          "
        >
          AI clinical analysis
        </p>

      </div>

      {/* ================================================= */}
      {/* INTERACTIONS */}
      {/* ================================================= */}

      <div
        className={`
          ${cardClass}
          bg-gradient-to-br
          from-rose-900/20
          to-orange-900/20
          hover:shadow-[0_0_35px_rgba(251,146,60,0.18)]
        `}
      >

        <div className="flex items-start justify-between">

          <div className="min-w-0">

            <p
              className="
                text-[11px]
                uppercase
                tracking-[0.35em]
                text-gray-400
              "
            >
              Interactions
            </p>

            <h2
              className="
                mt-8
                text-6xl
                font-black
                leading-none
                text-white
              "
            >
              {interactions}
            </h2>

          </div>

          <div
            className="
              shrink-0
              rounded-[24px]
              border
              border-white/10
              bg-white/5
              p-4
            "
          >
            <Activity
              size={34}
              className="text-orange-300"
            />
          </div>

        </div>

        <p
          className="
            mt-10
            text-base
            text-gray-400
          "
        >
          Potential conflicts
        </p>

      </div>

      {/* ================================================= */}
      {/* AI ENGINE */}
      {/* ================================================= */}

      <div
        className={`
          ${cardClass}
          bg-gradient-to-br
          from-indigo-900/30
          to-violet-900/30
          hover:shadow-[0_0_35px_rgba(168,85,247,0.18)]
        `}
      >

        <div className="flex items-start justify-between gap-4">

          <div className="min-w-0 flex-1">

            <p
              className="
                text-[11px]
                uppercase
                tracking-[0.35em]
                text-gray-400
              "
            >
              AI Engine
            </p>

            <h2
              className="
                mt-8
                text-5xl
                font-black
                leading-none
                text-white
                whitespace-nowrap
              "
            >
              Active
            </h2>

          </div>

          <div
            className="
              shrink-0
              rounded-[24px]
              border
              border-white/10
              bg-white/5
              p-4
            "
          >
            <BrainCircuit
              size={34}
              className="text-violet-300"
            />
          </div>

        </div>

        <p
          className="
            mt-10
            text-base
            text-gray-400
          "
        >
          Clinical intelligence
        </p>

      </div>

    </div>
  );
}