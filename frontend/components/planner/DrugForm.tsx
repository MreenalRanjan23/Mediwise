"use client";

import { useState } from "react";
import {
  Pill,
  ActivitySquare,
  Plus,
} from "lucide-react";

export default function DrugForm({ onAdd }: any) {

  const [name, setName] = useState("");
  const [dose, setDose] = useState("");

  const handleAdd = () => {

    if (!name.trim()) return;

    onAdd({
      name: name.trim(),
      dose: dose.trim(),
    });

    setName("");
    setDose("");
  };

  return (

    <div
      className="
        relative
        overflow-hidden
        rounded-[26px]
        border
        border-white/10
        bg-[#081120]/90
        p-6
        backdrop-blur-xl
      "
    >

      {/* BACKGROUND GLOW */}

      <div
        className="
          absolute
          inset-0
          bg-[radial-gradient(circle_at_top_right,rgba(59,130,246,0.12),transparent_40%)]
          pointer-events-none
        "
      />

      {/* CONTENT */}

      <div className="relative z-10">

        {/* HEADER */}

        <div className="flex items-center gap-4 mb-7">

          <div
            className="
              w-14
              h-14
              rounded-2xl
              bg-gradient-to-br
              from-blue-500/20
              to-purple-500/20
              border
              border-white/10
              flex
              items-center
              justify-center
            "
          >
            <Pill className="w-7 h-7 text-blue-300" />
          </div>

          <div>

            <h2 className="text-3xl font-black tracking-tight text-blue-400">
              Add Medication
            </h2>

            <p className="text-gray-500 mt-1 text-sm">
              Enter medication details for AI safety analysis
            </p>

          </div>

        </div>

        {/* DRUG INPUT */}

        <div className="relative mb-4">

          <div
            className="
              absolute
              left-5
              top-1/2
              -translate-y-1/2
              text-gray-500
            "
          >
            <Pill className="w-5 h-5" />
          </div>

          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Drug name"
            className="
              w-full
              pl-14
              pr-5
              py-4
              rounded-2xl
              border
              border-white/10
              bg-[#050816]
              text-white
              placeholder:text-gray-500
              text-base
              outline-none
              focus:border-blue-500/40
              focus:ring-4
              focus:ring-blue-500/10
              transition-all
            "
          />

        </div>

        {/* DOSE INPUT */}

        <div className="relative mb-6">

          <div
            className="
              absolute
              left-5
              top-1/2
              -translate-y-1/2
              text-gray-500
            "
          >
            <ActivitySquare className="w-5 h-5" />
          </div>

          <input
            value={dose}
            onChange={(e) => setDose(e.target.value)}
            placeholder="Dose (e.g. 500mg)"
            className="
              w-full
              pl-14
              pr-5
              py-4
              rounded-2xl
              border
              border-white/10
              bg-[#050816]
              text-white
              placeholder:text-gray-500
              text-base
              outline-none
              focus:border-purple-500/40
              focus:ring-4
              focus:ring-purple-500/10
              transition-all
            "
          />

        </div>

        {/* BUTTON */}

        <button
          onClick={handleAdd}
          className="
            group
            relative
            overflow-hidden
            w-full
            py-4
            rounded-2xl
            bg-gradient-to-r
            from-blue-500
            via-indigo-500
            to-purple-500
            text-lg
            font-semibold
            shadow-lg
            shadow-purple-500/20
            hover:shadow-purple-500/40
            hover:scale-[1.01]
            active:scale-[0.99]
            transition-all
            duration-300
          "
        >

          {/* BUTTON SHINE */}

          <div
            className="
              absolute
              inset-0
              bg-[linear-gradient(120deg,transparent,rgba(255,255,255,0.18),transparent)]
              translate-x-[-120%]
              group-hover:translate-x-[120%]
              transition-transform
              duration-1000
            "
          />

          <div className="relative flex items-center justify-center gap-2">

            <Plus className="w-5 h-5" />

            <span>Add Medication</span>

          </div>

        </button>

      </div>

    </div>
  );
}