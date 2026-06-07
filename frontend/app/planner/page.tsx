"use client";

import { useState } from "react";

import MainLayout from "@/components/layout/MainLayout";

import DrugForm from "@/components/planner/DrugForm";
import DrugList from "@/components/planner/DrugList";
import RiskPanel from "@/components/planner/RiskPanel";
import TopStats from "@/components/planner/TopStats";
import AnalyticsCharts from "@/components/planner/AnalyticsCharts";
import AIInsights from "@/components/planner/AIInsights";
import PatientProfileForm from "@/components/planner/PatientProfileForm";

import { analyzeMedicationPlan } from "@/lib/api";

export default function Planner() {

  // =================================================
  // STATE
  // =================================================

  const [drugs, setDrugs] =
    useState<any[]>([]);

  const [riskData, setRiskData] =
    useState<any>(null);

  const [loading, setLoading] =
    useState(false);

  // =================================================
  // PATIENT PROFILE
  // =================================================

  const [
    patientProfile,
    setPatientProfile,
  ] = useState({

    age: 45,

    sex: "M",

    weight: 70,

    smoker: false,

    alcohol_use: false,

    conditions: [],

    creatinine: 1.0,

    alt: 30,

    ast: 30,
  });

  // =================================================
  // RUN ANALYSIS
  // =================================================

  const runAnalysis = async (
    updatedDrugs: any[]
  ) => {

    try {

      setLoading(true);

      const payload = {

        drugs: updatedDrugs.map(
          (d) =>
            d.name.toLowerCase()
        ),

        age: patientProfile.age,

        sex: patientProfile.sex,

        weight:
          patientProfile.weight,

        smoker:
          patientProfile.smoker,

        alcohol_use:
          patientProfile.alcohol_use,

        conditions:
          patientProfile.conditions,

        creatinine:
          patientProfile.creatinine,

        alt: patientProfile.alt,

        ast: patientProfile.ast,
      };

      console.log(
        "PAYLOAD:",
        payload
      );

      const response =
        await analyzeMedicationPlan(
          payload
        );

      console.log(
        "API RESPONSE:",
        response
      );

      if (response?.success) {

        setRiskData(
          response.results
        );
      }

    } catch (error) {

      console.error(
        "Clinical analysis failed:",
        error
      );

    } finally {

      setLoading(false);
    }
  };

  // =================================================
  // ADD MEDICATION
  // =================================================

  const handleAddMedication =
    async (drug: any) => {

      const updatedDrugs = [
        ...drugs,
        drug,
      ];

      setDrugs(updatedDrugs);

      await runAnalysis(
        updatedDrugs
      );
    };

  // =================================================
  // REMOVE DRUG
  // =================================================

  const handleRemoveDrug =
    async (index: number) => {

      const updated =
        drugs.filter(
          (_, i) => i !== index
        );

      setDrugs(updated);

      await runAnalysis(updated);
    };

  // =================================================
  // SAFE FALLBACK DATA
  // =================================================

  const safeRiskData =
    riskData || {

      risk_analysis: {

        score: 0,

        normalized: {

          raw_score: 0,

          normalized_score: 0,

          risk_level: "Minimal",

          color: "#22c55e",
        },

        interactions: [],
      },

      toxicity_results: [],

      food_interactions: [],

      alternatives: [],

      insights: [],

      lab_analysis: {},

      risk_breakdown: {},

      explanations: [],

      analytics: {

        risk_distribution: {

          safe: 100,

          moderate: 0,

          high: 0,
        },

        organ_toxicity: {

          liver: 0,

          kidney: 0,

          cardiac: 0,

          cns: 0,
        },

        weekly_trend: [],
      },
    };

  // =================================================
  // RISK VALUES
  // =================================================

  const normalizedScore =
    safeRiskData?.risk_analysis
      ?.normalized
      ?.normalized_score || 0;

  const rawScore =
    safeRiskData?.risk_analysis
      ?.score || 0;

  const riskLevel =
    safeRiskData?.risk_analysis
      ?.normalized
      ?.risk_level || "Minimal";

  // =================================================
  // INTERACTION COUNT
  // =================================================

  const interactionCount =
    safeRiskData?.risk_analysis
      ?.interactions?.length || 0;

  // =================================================
  // UI
  // =================================================

  return (

    <MainLayout>

      <div
        className="
          relative
          min-h-screen
          overflow-hidden
          bg-[#030712]
          text-white
        "
      >

        {/* ================================================= */}
        {/* BACKGROUND GLOWS */}
        {/* ================================================= */}

        <div
          className="
            absolute
            inset-0
            overflow-hidden
            pointer-events-none
          "
        >

          {/* BLUE */}

          <div
            className="
              absolute
              top-[-180px]
              left-[10%]
              h-[500px]
              w-[500px]
              rounded-full
              bg-blue-500/10
              blur-[140px]
            "
          />

          {/* PURPLE */}

          <div
            className="
              absolute
              top-[180px]
              right-[-180px]
              h-[480px]
              w-[480px]
              rounded-full
              bg-purple-500/10
              blur-[140px]
            "
          />

          {/* CYAN */}

          <div
            className="
              absolute
              bottom-[-240px]
              left-[35%]
              h-[550px]
              w-[550px]
              rounded-full
              bg-cyan-500/10
              blur-[140px]
            "
          />

        </div>

        {/* ================================================= */}
        {/* PAGE CONTENT */}
        {/* ================================================= */}

        <div className="relative z-10 p-6 xl:p-8">

          {/* ================================================= */}
          {/* HEADER */}
          {/* ================================================= */}

          <div className="mb-8 fade-in-up">

            <h1
              className="
                text-4xl
                xl:text-5xl
                font-black
                tracking-tight
                bg-gradient-to-r
                from-white
                via-blue-100
                to-purple-200
                bg-clip-text
                text-transparent
              "
            >
              Medication Planner
            </h1>

            <p
              className="
                mt-3
                max-w-2xl
                text-base
                leading-relaxed
                text-gray-400
              "
            >
              AI-powered medication
              safety, interaction
              analysis, and
              intelligent clinical
              recommendations.
            </p>

          </div>

          {/* ================================================= */}
          {/* PATIENT PROFILE */}
          {/* ================================================= */}

          <div className="mb-6">

            <PatientProfileForm
              patientProfile={
                patientProfile
              }
              setPatientProfile={
                setPatientProfile
              }
            />

          </div>

          {/* ================================================= */}
          {/* TOP STATS */}
          {/* ================================================= */}

          <div className="mb-6 fade-in-up">

            <TopStats
              drugs={drugs}
              riskData={
                safeRiskData
              }
            />

          </div>

          {/* ================================================= */}
          {/* MAIN GRID */}
          {/* ================================================= */}

          <div
            className="
              grid
              grid-cols-1
              xl:grid-cols-[minmax(0,1fr)_380px]
              gap-6
              items-start
            "
          >

            {/* ================================================= */}
            {/* LEFT COLUMN */}
            {/* ================================================= */}

            <div className="space-y-6 min-w-0">

              {/* ADD MEDICATION */}

              <DrugForm
                onAdd={
                  handleAddMedication
                }
              />

              {/* DRUG LIST */}

              <DrugList
                drugs={drugs}
                onRemove={
                  handleRemoveDrug
                }
              />

              {/* AI INSIGHTS */}

              <AIInsights
                insights={
                  safeRiskData.insights
                }
                loading={loading}
              />

              {/* ANALYTICS */}

              <AnalyticsCharts
                data={safeRiskData}
              />

            </div>

            {/* ================================================= */}
            {/* RIGHT COLUMN */}
            {/* ================================================= */}

            <div className="space-y-6 min-w-0">

              {/* RISK PANEL */}

              <RiskPanel
                riskData={
                  safeRiskData
                }
                loading={loading}
              />

              {/* RISK SUMMARY */}

              <div
                className="
                  rounded-[28px]
                  border
                  border-white/10
                  bg-[#0B1120]/90
                  p-6
                  backdrop-blur-xl
                "
              >

                <h3
                  className="
                    text-2xl
                    font-bold
                    text-white
                  "
                >
                  Clinical Summary
                </h3>

                <div className="mt-6 space-y-5">

                  <div>

                    <p className="text-sm text-gray-400">
                      Normalized Risk
                    </p>

                    <p
                      className="
                        mt-1
                        text-4xl
                        font-black
                        text-white
                      "
                    >
                      {normalizedScore}%
                    </p>

                  </div>

                  <div>

                    <p className="text-sm text-gray-400">
                      Raw Risk Score
                    </p>

                    <p
                      className="
                        mt-1
                        text-2xl
                        font-bold
                        text-blue-300
                      "
                    >
                      {rawScore.toFixed(2)}
                    </p>

                  </div>

                  <div>

                    <p className="text-sm text-gray-400">
                      Risk Level
                    </p>

                    <p
                      className="
                        mt-1
                        text-xl
                        font-semibold
                        text-yellow-300
                      "
                    >
                      {riskLevel}
                    </p>

                  </div>

                  <div>

                    <p className="text-sm text-gray-400">
                      Drug Interactions
                    </p>

                    <p
                      className="
                        mt-1
                        text-xl
                        font-semibold
                        text-red-300
                      "
                    >
                      {interactionCount}
                    </p>

                  </div>

                </div>

              </div>

            </div>

          </div>

        </div>

      </div>

    </MainLayout>
  );
}