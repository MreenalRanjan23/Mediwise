"use client";

import {
  ShieldCheck,
  ShieldAlert,
  ShieldX,
  AlertTriangle,
  Pill,
} from "lucide-react";

export default function RiskPanel({ riskData }: any) {

  // =================================================
  // NORMALIZED RISK
  // =================================================

  const normalized =
    riskData?.risk_analysis?.normalized || {};

  const risk =
    normalized?.normalized_score ?? 0;

  const riskLevel =
    normalized?.risk_level ?? "Low";

  // =================================================
  // INTERACTIONS
  // =================================================

  const interactions =
    riskData?.risk_analysis?.interactions ?? [];

  // =================================================
  // ALTERNATIVES
  // =================================================

  const alternatives =
    riskData?.alternatives ?? [];

  // =================================================
  // RISK COLOR
  // =================================================

  const getColor = () => {

    if (risk < 30) return "#34d399";

    if (risk < 70) return "#facc15";

    return "#f87171";
  };

  // =================================================
  // ICON
  // =================================================

  const RiskIcon =
    risk < 30
      ? ShieldCheck
      : risk < 70
      ? ShieldAlert
      : ShieldX;

  // =================================================
  // SVG RING
  // =================================================

  const radius = 58;

  const circumference =
    2 * Math.PI * radius;

  const progress =
    circumference -
    (risk / 100) * circumference;

  return (

    <div className="w-full flex flex-col gap-6">

      {/* ================================================= */}
      {/* RISK OVERVIEW */}
      {/* ================================================= */}

      <div
        className="
          group
          relative
          overflow-hidden
          rounded-[32px]
          border
          border-white/10
          bg-gradient-to-br
          from-[#111827]/95
          via-[#0F172A]/95
          to-[#081028]/95
          p-6
          backdrop-blur-2xl
          shadow-2xl
        "
      >

        {/* GLOW */}
        <div
          className="
            absolute
            top-0
            right-0
            h-40
            w-40
            rounded-full
            blur-3xl
            opacity-20
          "
          style={{
            backgroundColor: getColor(),
          }}
        />

        {/* CONTENT */}
        <div className="relative z-10">

          {/* HEADER */}
          <div className="flex items-start justify-between">

            <div>

              <h2
                className="
                  text-4xl
                  font-black
                  leading-tight
                  text-white
                "
              >
                Risk
                <br />
                Analysis
              </h2>

              <p
                className="
                  mt-4
                  max-w-[260px]
                  text-gray-400
                  text-base
                  leading-relaxed
                "
              >
                AI-generated medication safety
                score
              </p>

            </div>

            <div
              className="
                rounded-[24px]
                border
                border-white/10
                bg-white/[0.04]
                p-4
                backdrop-blur-xl
              "
            >
              <RiskIcon
                size={34}
                style={{
                  color: getColor(),
                }}
              />
            </div>

          </div>

          {/* MAIN CONTENT */}
          <div
            className="
              mt-10
              flex
              items-center
              justify-between
              gap-6
            "
          >

            {/* LEFT */}
            <div>

              <div
                className="
                  text-7xl
                  font-black
                  leading-none
                "
                style={{
                  color: getColor(),
                }}
              >
                {risk}%
              </div>

              <div
                className="
                  mt-4
                  text-3xl
                  font-bold
                  text-white
                "
              >
                {riskLevel} Risk
              </div>

              <p
                className="
                  mt-4
                  max-w-[220px]
                  text-gray-400
                  leading-relaxed
                "
              >
                Based on toxicity,
                interactions,
                patient conditions,
                and AI clinical analysis.
              </p>

            </div>

            {/* RIGHT RING */}
            <div
              className="
                relative
                flex
                items-center
                justify-center
              "
            >

              {/* OUTER GLOW */}
              <div
                className="
                  absolute
                  h-48
                  w-48
                  rounded-full
                  blur-3xl
                  opacity-10
                "
                style={{
                  backgroundColor: getColor(),
                }}
              />

              <svg
                width="170"
                height="170"
                className="-rotate-90"
              >

                {/* TRACK */}
                <circle
                  cx="85"
                  cy="85"
                  r={radius}
                  stroke="rgba(255,255,255,0.08)"
                  strokeWidth="12"
                  fill="transparent"
                />

                {/* PROGRESS */}
                <circle
                  cx="85"
                  cy="85"
                  r={radius}
                  stroke={getColor()}
                  strokeWidth="12"
                  fill="transparent"
                  strokeLinecap="round"
                  strokeDasharray={circumference}
                  strokeDashoffset={progress}
                  style={{
                    transition:
                      "stroke-dashoffset 1s ease",
                  }}
                />

              </svg>

              {/* CENTER */}
              <div
                className="
                  absolute
                  flex
                  flex-col
                  items-center
                "
              >

                <div
                  className="
                    text-4xl
                    font-black
                    text-white
                  "
                >
                  {risk}%
                </div>

                <div
                  className="
                    text-sm
                    text-gray-400
                  "
                >
                  Overall
                </div>

              </div>

            </div>

          </div>

        </div>

      </div>

      {/* ================================================= */}
      {/* DRUG INTERACTIONS */}
      {/* ================================================= */}

      <div
        className="
          relative
          overflow-hidden
          rounded-[32px]
          border
          border-white/10
          bg-gradient-to-br
          from-[#111827]/95
          via-[#0F172A]/95
          to-[#081028]/95
          p-6
          backdrop-blur-2xl
          shadow-2xl
        "
      >

        <div className="flex items-start gap-4">

          <div
            className="
              rounded-[24px]
              border
              border-red-500/20
              bg-red-500/10
              p-4
            "
          >
            <AlertTriangle
              size={30}
              className="text-red-400"
            />
          </div>

          <div>

            <h3
              className="
                text-4xl
                font-black
                leading-tight
                text-white
              "
            >
              Drug
              <br />
              Interactions
            </h3>

            <p
              className="
                mt-4
                text-gray-400
              "
            >
              Potential medication conflicts
            </p>

          </div>

        </div>

        <div className="mt-8">

          {interactions.length === 0 ? (

            <div
              className="
                rounded-[24px]
                border
                border-white/10
                bg-white/[0.03]
                px-6
                py-5
                text-gray-400
              "
            >
              No interactions detected
            </div>

          ) : (

            <div className="space-y-4">

              {interactions.map(
                (interaction: any, index: number) => (

                  <div
                    key={index}
                    className="
                      rounded-[24px]
                      border
                      border-red-500/20
                      bg-red-500/10
                      p-5
                    "
                  >

                    <div className="text-white font-semibold">

                      {interaction.drug_a}
                      {" + "}
                      {interaction.drug_b}

                    </div>

                  </div>
                )
              )}

            </div>
          )}

        </div>

      </div>

      {/* ================================================= */}
      {/* SAFER ALTERNATIVES */}
      {/* ================================================= */}

      <div
        className="
          relative
          overflow-hidden
          rounded-[32px]
          border
          border-white/10
          bg-gradient-to-br
          from-[#111827]/95
          via-[#0F172A]/95
          to-[#081028]/95
          p-6
          backdrop-blur-2xl
          shadow-2xl
        "
      >

        <div className="flex items-start gap-4">

          <div
            className="
              rounded-[24px]
              border
              border-cyan-500/20
              bg-cyan-500/10
              p-4
            "
          >
            <Pill
              size={30}
              className="text-cyan-400"
            />
          </div>

          <div>

            <h3
              className="
                text-4xl
                font-black
                leading-tight
                text-white
              "
            >
              Safer
              <br />
              Alternatives
            </h3>

            <p
              className="
                mt-4
                text-gray-400
              "
            >
              AI medication recommendations
            </p>

          </div>

        </div>

        <div className="mt-8">

          {alternatives.length === 0 ? (

            <div
              className="
                rounded-[24px]
                border
                border-white/10
                bg-white/[0.03]
                px-6
                py-5
                text-gray-400
              "
            >
              No safer alternatives available
            </div>

          ) : (

            <div className="space-y-4">

              {alternatives.map(
                (item: any, index: number) => (

                  <div
                    key={index}
                    className="
                      rounded-[24px]
                      border
                      border-cyan-500/20
                      bg-cyan-500/10
                      p-5
                    "
                  >

                    <div className="text-white font-semibold">

                      {item.drug}

                    </div>

                    <div
                      className="
                        mt-2
                        text-sm
                        text-cyan-200
                      "
                    >

                      {item.alternatives?.join(", ")}

                    </div>

                  </div>
                )
              )}

            </div>
          )}

        </div>

      </div>

    </div>
  );
}