"use client";

import {
  Pill,
  ShieldCheck,
  Clock3,
  Trash2,
} from "lucide-react";

export default function DrugList({
  drugs,
  onRemove,
}: any) {

  return (

    <div
      className="
        relative
        overflow-hidden
        rounded-[28px]
        border
        border-white/10
        bg-gradient-to-br
        from-[#111827]
        to-[#081028]
        p-6
        shadow-[0_0_50px_rgba(6,182,212,0.08)]
        backdrop-blur-xl
      "
    >

      {/* GLOW */}
      <div
        className="
          absolute
          inset-0
          bg-gradient-to-br
          from-cyan-500/5
          to-blue-500/5
          pointer-events-none
        "
      />

      {/* CONTENT */}
      <div className="relative z-10">

        {/* HEADER */}
        <div className="flex items-start justify-between mb-6">

          <div>
            <h2 className="text-4xl font-black tracking-tight text-white">
              Medications
            </h2>
            <p className="text-gray-400 mt-2 text-lg">
              Current active medication plan
            </p>
          </div>

          {/* ACTIVE COUNT */}
          <div
            className="
              shrink-0
              px-5
              py-3
              rounded-2xl
              border
              border-blue-500/20
              bg-blue-500/10
              text-center
            "
          >
            <h3 className="text-3xl font-black text-white">
              {drugs.length}
            </h3>
            <p className="text-blue-300 text-lg mt-1">
              Active
            </p>
          </div>

        </div>

        {/* DRUG LIST */}
        {drugs && drugs.length > 0 ? (

          <div className="space-y-5">

            {drugs.map((drug: any, index: number) => (

              <div
                key={index}
                className="
                  relative
                  group
                  rounded-[28px]
                  border
                  border-white/10
                  bg-[#0A1020]/90
                  p-5
                  transition-all
                  duration-300
                  hover:border-cyan-500/20
                  hover:shadow-[0_0_30px_rgba(6,182,212,0.12)]
                "
              >

                {/* REMOVE BUTTON — absolutely positioned top-right */}
                <button
                  onClick={() => onRemove(index)}
                  className="
                    absolute
                    top-5
                    right-5
                    flex
                    items-center
                    gap-2
                    px-4
                    py-2
                    rounded-2xl
                    bg-red-500/10
                    border
                    border-red-500/20
                    text-red-400
                    text-sm
                    font-medium
                    hover:bg-red-500
                    hover:text-white
                    transition-all
                    z-10
                  "
                >
                  <Trash2 className="w-4 h-4" />
                  Remove
                </button>

                {/* TOP ROW: icon + name — name gets all the space it needs */}
                <div className="flex items-center gap-4 mb-4 pr-32">

                  {/* ICON */}
                  <div
                    className="
                      h-16
                      w-16
                      rounded-2xl
                      bg-gradient-to-br
                      from-blue-500/20
                      to-purple-500/20
                      border
                      border-white/10
                      flex
                      items-center
                      justify-center
                      shrink-0
                    "
                  >
                    <Pill className="w-8 h-8 text-pink-300" />
                  </div>

                  {/* NAME — full width, wraps naturally if very long */}
                  <h3
                    className="
                      text-2xl
                      font-bold
                      text-white
                      capitalize
                      leading-tight
                    "
                  >
                    {drug.name}
                  </h3>

                </div>

                {/* TAGS ROW — always horizontal, indented under name */}
                <div className="flex items-center gap-3 flex-wrap pl-20">

                  {/* DOSE */}
                  <div
                    className="
                      px-4
                      py-2
                      rounded-xl
                      bg-blue-500/10
                      border
                      border-blue-500/20
                      text-blue-300
                      text-sm
                      flex
                      items-center
                      gap-2
                      whitespace-nowrap
                    "
                  >
                    <ShieldCheck className="w-4 h-4 shrink-0" />
                    {drug.dose ? drug.dose : "Dose not specified"}
                  </div>

                  {/* TIME */}
                  <div
                    className="
                      px-4
                      py-2
                      rounded-xl
                      bg-purple-500/10
                      border
                      border-purple-500/20
                      text-purple-300
                      text-sm
                      flex
                      items-center
                      gap-2
                      whitespace-nowrap
                    "
                  >
                    <Clock3 className="w-4 h-4 shrink-0" />
                    Morning
                  </div>

                  {/* STATUS */}
                  <div
                    className="
                      px-4
                      py-2
                      rounded-xl
                      bg-emerald-500/10
                      border
                      border-emerald-500/20
                      text-emerald-300
                      text-sm
                      flex
                      items-center
                      gap-2
                      whitespace-nowrap
                    "
                  >
                    <div className="w-2 h-2 rounded-full bg-emerald-400 shrink-0" />
                    Safe
                  </div>

                </div>

              </div>

            ))}

          </div>

        ) : (

          <div
            className="
              flex
              flex-col
              items-center
              justify-center
              py-20
              rounded-3xl
              border
              border-dashed
              border-white/10
              bg-[#050816]
            "
          >
            <div className="text-6xl mb-5 opacity-70">💊</div>
            <h3 className="text-2xl font-semibold text-white mb-2">
              No medications added
            </h3>
            <p className="text-gray-500 text-center max-w-md">
              Start building your medication plan by adding your first medicine above.
            </p>
          </div>

        )}

      </div>

    </div>
  );
}