"use client";

import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  Tooltip,
  BarChart,
  Bar,
} from "recharts";

const COLORS = [
  "#22c55e",
  "#facc15",
  "#ef4444",
];

interface Props {
  data?: any;
}

export default function AnalyticsCharts({
  data,
}: Props) {

  // =================================================
  // BACKEND ANALYTICS
  // =================================================

  const analytics =
    data?.analytics || {};

  const distribution =
    analytics?.risk_distribution || {};

  const organToxicity =
    analytics?.organ_toxicity || {};

  const weeklyTrend =
    analytics?.weekly_trend || [];

  // =================================================
  // SAFE VALUES
  // =================================================

  const safe =
    Number(distribution?.safe || 0);

  const moderate =
    Number(distribution?.moderate || 0);

  const high =
    Number(distribution?.high || 0);

  // =================================================
  // FALLBACKS
  // =================================================

  const riskDistribution =
    safe + moderate + high > 0
      ? [
          {
            name: "Safe",
            value: safe,
          },
          {
            name: "Moderate",
            value: moderate,
          },
          {
            name: "High",
            value: high,
          },
        ]
      : [
          {
            name: "Safe",
            value: 100,
          },
        ];

  const toxicityData = [
    {
      organ: "Liver",
      level: Number(
        organToxicity?.liver || 0
      ),
    },
    {
      organ: "Kidney",
      level: Number(
        organToxicity?.kidney || 0
      ),
    },
    {
      organ: "Cardiac",
      level: Number(
        organToxicity?.cardiac || 0
      ),
    },
    {
      organ: "CNS",
      level: Number(
        organToxicity?.cns || 0
      ),
    },
  ];

  const trendData =
    weeklyTrend.length > 0
      ? weeklyTrend
      : [
          {
            day: "Mon",
            risk: 10,
          },
          {
            day: "Tue",
            risk: 20,
          },
          {
            day: "Wed",
            risk: 35,
          },
          {
            day: "Thu",
            risk: 50,
          },
          {
            day: "Fri",
            risk: 40,
          },
          {
            day: "Sat",
            risk: 25,
          },
          {
            day: "Sun",
            risk: 15,
          },
        ];

  return (

    <div className="space-y-6 w-full">

      {/* ================================================= */}
      {/* TOP SECTION */}
      {/* ================================================= */}

      <div
        className="
          grid
          grid-cols-1
          xl:grid-cols-2
          gap-6
          items-stretch
          w-full
        "
      >

        {/* ================================================= */}
        {/* RISK DISTRIBUTION */}
        {/* ================================================= */}

        <div
          className="
            group
            relative
            overflow-hidden
            rounded-[28px]
            border
            border-white/10
            bg-[#0B1120]/90
            p-6
            backdrop-blur-xl
            transition-all
            duration-300
            hover:-translate-y-1
            hover:border-white/20
            hover:shadow-[0_0_40px_rgba(59,130,246,0.18)]
            min-w-0
          "
        >

          {/* HOVER GLOW */}

          <div
            className="
              absolute
              inset-0
              opacity-0
              transition-opacity
              duration-500
              group-hover:opacity-100
              bg-[radial-gradient(circle_at_top_right,rgba(59,130,246,0.12),transparent_45%)]
              pointer-events-none
            "
          />

          {/* BACKGROUND GLOW */}

          <div
            className="
              absolute
              top-0
              right-0
              h-40
              w-40
              rounded-full
              bg-green-500/10
              blur-3xl
            "
          />

          <div className="relative z-10">

            <h3
              className="
                text-3xl
                font-black
                text-white
                tracking-tight
              "
            >
              Risk Distribution
            </h3>

            <p
              className="
                mt-2
                text-gray-400
                text-base
              "
            >
              AI analyzed medication safety
            </p>

            {/* CHART */}

            <div
              className="
                mt-8
                h-[320px]
                w-full
                flex
                items-center
                justify-center
                overflow-visible
              "
            >

              <PieChart width={300} height={300}>

                <Pie
                  data={riskDistribution}
                  cx="50%"
                  cy="50%"
                  innerRadius={65}
                  outerRadius={105}
                  paddingAngle={3}
                  dataKey="value"
                  stroke="#0B1120"
                  strokeWidth={2}
                >

                  {riskDistribution.map(
                    (
                      entry,
                      index
                    ) => (

                      <Cell
                        key={`cell-${index}`}
                        fill={
                          COLORS[
                            index %
                              COLORS.length
                          ]
                        }
                      />
                    )
                  )}

                </Pie>

                <Tooltip />

              </PieChart>

            </div>

            {/* LEGEND */}

            <div className="space-y-4">

              {riskDistribution.map(
                (item, index) => (

                  <div
                    key={item.name}
                    className="
                      flex
                      items-center
                      justify-between
                    "
                  >

                    <div
                      className="
                        flex
                        items-center
                        gap-3
                      "
                    >

                      <div
                        className="
                          h-5
                          w-5
                          rounded-full
                        "
                        style={{
                          backgroundColor:
                            COLORS[index],
                        }}
                      />

                      <span
                        className="
                          text-2xl
                          text-gray-200
                        "
                      >
                        {item.name}
                      </span>

                    </div>

                    <span
                      className="
                        text-2xl
                        font-bold
                        text-white
                      "
                    >
                      {item.value}%
                    </span>

                  </div>
                )
              )}

            </div>

          </div>

        </div>

        {/* ================================================= */}
        {/* WEEKLY TREND */}
        {/* ================================================= */}

        <div
          className="
            group
            relative
            overflow-hidden
            rounded-[28px]
            border
            border-white/10
            bg-[#0B1120]/90
            p-6
            backdrop-blur-xl
            transition-all
            duration-300
            hover:-translate-y-1
            hover:border-white/20
            hover:shadow-[0_0_40px_rgba(59,130,246,0.18)]
            min-w-0
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
              bg-blue-500/10
              blur-3xl
            "
          />

          <div className="relative z-10">

            <h3
              className="
                text-3xl
                font-black
                text-white
                tracking-tight
              "
            >
              Weekly Risk Trend
            </h3>

            <p
              className="
                mt-2
                text-gray-400
                text-base
              "
            >
              Clinical interaction fluctuation
            </p>

            <div className="mt-10 h-[420px] w-full">

              <ResponsiveContainer
                width="100%"
                height="100%"
              >

                <AreaChart data={trendData}>

                  <defs>

                    <linearGradient
                      id="riskGradient"
                      x1="0"
                      y1="0"
                      x2="0"
                      y2="1"
                    >

                      <stop
                        offset="5%"
                        stopColor="#3b82f6"
                        stopOpacity={0.4}
                      />

                      <stop
                        offset="95%"
                        stopColor="#3b82f6"
                        stopOpacity={0}
                      />

                    </linearGradient>

                  </defs>

                  <XAxis
                    dataKey="day"
                    stroke="#94a3b8"
                    tickLine={false}
                    axisLine={false}
                  />

                  <Tooltip />

                  <Area
                    type="monotone"
                    dataKey="risk"
                    stroke="#3b82f6"
                    strokeWidth={4}
                    fill="url(#riskGradient)"
                  />

                </AreaChart>

              </ResponsiveContainer>

            </div>

          </div>

        </div>

      </div>

      {/* ================================================= */}
      {/* ORGAN TOXICITY */}
      {/* ================================================= */}

      <div
        className="
          group
          relative
          overflow-hidden
          rounded-[28px]
          border
          border-white/10
          bg-[#0B1120]/90
          p-6
          backdrop-blur-xl
          transition-all
          duration-300
          hover:-translate-y-1
          hover:border-white/20
          hover:shadow-[0_0_40px_rgba(239,68,68,0.14)]
        "
      >

        {/* GLOW */}

        <div
          className="
            absolute
            bottom-0
            left-0
            h-40
            w-40
            rounded-full
            bg-red-500/10
            blur-3xl
          "
        />

        <div className="relative z-10">

          <h3
            className="
              text-3xl
              font-black
              text-white
              tracking-tight
            "
          >
            Organ Toxicity Load
          </h3>

          <p
            className="
              mt-2
              text-gray-400
              text-base
            "
          >
            AI-estimated physiological stress
          </p>

          <div className="mt-10 h-[420px] w-full">

            <ResponsiveContainer
              width="100%"
              height="100%"
            >

              <BarChart data={toxicityData}>

                <XAxis
                  dataKey="organ"
                  stroke="#94a3b8"
                  tickLine={false}
                  axisLine={false}
                />

                <Tooltip />

                <Bar
                  dataKey="level"
                  radius={[18, 18, 0, 0]}
                  fill="#ef4444"
                />

              </BarChart>

            </ResponsiveContainer>

          </div>

        </div>

      </div>

    </div>
  );
}