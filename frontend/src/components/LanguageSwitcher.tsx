"use client";

import React from "react";
import { useLanguage } from "../context/LanguageContext";

export default function LanguageSwitcher() {
    const { language, setLanguage } = useLanguage();

    return (
        <button
            onClick={() => setLanguage(language === "en" ? "ur" : "en")}
            className="px-3 py-1 rounded-md text-sm font-medium transition-colors bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-200"
            title={language === "en" ? "Switch to Urdu" : "Switch to English"}
        >
            {language === "en" ? "🇺🇸 English" : "🇵🇰 اردو"}
        </button>
    );
}
