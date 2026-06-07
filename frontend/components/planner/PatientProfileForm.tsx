"use client";

import {
  User,
  Activity,
  HeartPulse,
  FlaskConical,
} from "lucide-react";

interface Props {
  patientProfile: any;
  setPatientProfile: (profile: any) => void;
}

export default function PatientProfileForm({
  patientProfile,
  setPatientProfile,
}: Props) {

  // =================================================
  // UPDATE FIELD
  // =================================================

  const updateField = (
    field: string,
    value: any
  ) => {

    setPatientProfile({
      ...patientProfile,
      [field]: value,
    });
  };

  // =================================================
  // CONDITIONS
  // =================================================

  const toggleCondition = (
    condition: string
  ) => {

    const conditions =
      patientProfile.conditions || [];

    if (conditions.includes(condition)) {

      updateField(
        "conditions",
        conditions.filter(
          (c: string) => c !== condition
        )
      );

    } else {

      updateField(
        "conditions",
        [...conditions, condition]
      );
    }
  };

  // =================================================
  // UI
  // =================================================

  return (

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
        p-8
        backdrop-blur-2xl
        shadow-2xl
      "
    >

      {/* HEADER */}
      <div className="flex items-center gap-5">

        <div
          className="
            rounded-[24px]
            border
            border-cyan-500/20
            bg-cyan-500/10
            p-4
          "
        >
          <User
            size={34}
            className="text-cyan-400"
          />
        </div>

        <div>

          <h2
            className="
              text-5xl
              font-black
              text-white
            "
          >
            Patient Profile
          </h2>

          <p
            className="
              mt-2
              text-gray-400
              text-lg
            "
          >
            Personalized clinical intake
          </p>

        </div>

      </div>

      {/* GRID */}
      <div
        className="
          mt-10
          grid
          grid-cols-1
          xl:grid-cols-2
          gap-8
        "
      >

        {/* DEMOGRAPHICS */}
        <div
          className="
            rounded-[28px]
            border
            border-white/10
            bg-white/[0.03]
            p-6
          "
        >

          <div className="flex items-center gap-3 mb-6">

            <Activity className="text-cyan-400" />

            <h3
              className="
                text-2xl
                font-bold
                text-white
              "
            >
              Demographics
            </h3>

          </div>

          <div className="space-y-5">

            {/* AGE */}
            <input
              type="number"
              placeholder="Age"
              value={patientProfile.age || ""}
              onChange={(e) =>
                updateField(
                  "age",
                  Number(e.target.value)
                )
              }
              className="
                w-full
                rounded-2xl
                border
                border-white/10
                bg-[#020617]
                px-5
                py-4
                text-white
                outline-none
              "
            />

            {/* SEX */}
            <select
              value={patientProfile.sex || ""}
              onChange={(e) =>
                updateField(
                  "sex",
                  e.target.value
                )
              }
              className="
                w-full
                rounded-2xl
                border
                border-white/10
                bg-[#020617]
                px-5
                py-4
                text-white
                outline-none
              "
            >
              <option value="">
                Select Sex
              </option>

              <option value="M">
                Male
              </option>

              <option value="F">
                Female
              </option>

            </select>

            {/* WEIGHT */}
            <input
              type="number"
              placeholder="Weight (kg)"
              value={patientProfile.weight || ""}
              onChange={(e) =>
                updateField(
                  "weight",
                  Number(e.target.value)
                )
              }
              className="
                w-full
                rounded-2xl
                border
                border-white/10
                bg-[#020617]
                px-5
                py-4
                text-white
                outline-none
              "
            />

          </div>

        </div>

        {/* CONDITIONS */}
        <div
          className="
            rounded-[28px]
            border
            border-white/10
            bg-white/[0.03]
            p-6
          "
        >

          <div className="flex items-center gap-3 mb-6">

            <HeartPulse className="text-pink-400" />

            <h3
              className="
                text-2xl
                font-bold
                text-white
              "
            >
              Conditions
            </h3>

          </div>

          <div className="flex flex-wrap gap-4">

            {[
              "hypertension",
              "diabetes",
              "asthma",
              "kidney disease",
              "liver disease",
            ].map((condition) => (

              <button
                key={condition}
                onClick={() =>
                  toggleCondition(condition)
                }
                className={`
                  rounded-2xl
                  px-5
                  py-3
                  text-sm
                  font-semibold
                  transition-all

                  ${
                    patientProfile.conditions?.includes(
                      condition
                    )
                      ? "bg-cyan-500 text-white"
                      : "bg-[#020617] text-gray-400 border border-white/10"
                  }
                `}
              >
                {condition}
              </button>

            ))}

          </div>

          {/* LIFESTYLE */}
          <div className="mt-8 space-y-4">

            <label className="flex items-center gap-3 text-white">

              <input
                type="checkbox"
                checked={patientProfile.smoker || false}
                onChange={(e) =>
                  updateField(
                    "smoker",
                    e.target.checked
                  )
                }
              />

              Smoker

            </label>

            <label className="flex items-center gap-3 text-white">

              <input
                type="checkbox"
                checked={patientProfile.alcohol_use || false}
                onChange={(e) =>
                  updateField(
                    "alcohol_use",
                    e.target.checked
                  )
                }
              />

              Alcohol Use

            </label>

          </div>

        </div>

      </div>

      {/* LAB VALUES */}
      <div
        className="
          mt-8
          rounded-[28px]
          border
          border-white/10
          bg-white/[0.03]
          p-6
        "
      >

        <div className="flex items-center gap-3 mb-6">

          <FlaskConical className="text-yellow-400" />

          <h3
            className="
              text-2xl
              font-bold
              text-white
            "
          >
            Lab Values
          </h3>

        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">

          {/* CREATININE */}
          <div>

            <label className="mb-2 block text-sm text-gray-400">
              Creatinine (mg/dL)
            </label>

            <input
              type="number"
              placeholder="1.2"
              value={patientProfile.creatinine || ""}
              onChange={(e) =>
                updateField(
                  "creatinine",
                  Number(e.target.value)
                )
              }
              className="
                w-full
                rounded-2xl
                border
                border-white/10
                bg-[#020617]
                px-5
                py-4
                text-white
                outline-none
              "
            />

          </div>

          {/* ALT */}
          <div>

            <label className="mb-2 block text-sm text-gray-400">
              ALT / SGPT
            </label>

            <input
              type="number"
              placeholder="30"
              value={patientProfile.alt || ""}
              onChange={(e) =>
                updateField(
                  "alt",
                  Number(e.target.value)
                )
              }
              className="
                w-full
                rounded-2xl
                border
                border-white/10
                bg-[#020617]
                px-5
                py-4
                text-white
                outline-none
              "
            />

          </div>

          {/* AST */}
          <div>

            <label className="mb-2 block text-sm text-gray-400">
              AST / SGOT
            </label>

            <input
              type="number"
              placeholder="30"
              value={patientProfile.ast || ""}
              onChange={(e) =>
                updateField(
                  "ast",
                  Number(e.target.value)
                )
              }
              className="
                w-full
                rounded-2xl
                border
                border-white/10
                bg-[#020617]
                px-5
                py-4
                text-white
                outline-none
              "
            />

          </div>

        </div>

      </div>

    </div>
  );
}