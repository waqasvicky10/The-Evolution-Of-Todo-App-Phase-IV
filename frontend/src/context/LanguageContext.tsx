"use client";

import React, { createContext, useContext, useState, useEffect } from "react";

type Language = "en" | "ur";

interface LanguageContextType {
    language: Language;
    setLanguage: (lang: Language) => void;
    t: (key: string) => string;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export const translations = {
    en: {
        "nav.home": "Home",
        "nav.dashboard": "Dashboard",
        "nav.chat": "AI Chat",
        "nav.login": "Login",
        "nav.register": "Register",
        "nav.logout": "Logout",
        "chat.input.placeholder": "Type or speak your message...",
        "chat.listening": "Listening...",
        "chat.voice.en": "English (US)",
        "chat.voice.ur": "Urdu (PK)",
        "landing.title": "Todo App",
        "landing.subtitle": "Phase II - Full-Stack Web Application",
        "landing.description": "A modern, multi-user todo application with secure authentication and persistent storage.",
        "landing.secure": "Secure",
        "landing.persistent": "Persistent",
        "landing.multiuser": "Multi-User",
        "landing.getstarted": "Get Started",
        "landing.signin": "Sign In"
    },
    ur: {
        "nav.home": "ہوم",
        "nav.dashboard": "ڈیش بورڈ",
        "nav.chat": "AI چیٹ",
        "nav.login": "لاگ ان",
        "nav.register": "رجسٹر",
        "nav.logout": "لاگ آؤٹ",
        "chat.input.placeholder": "اپنا پیغام لکھیں یا بولیں...",
        "chat.listening": "سن رہا ہے...",
        "chat.voice.en": "انگریزی (US)",
        "chat.voice.ur": "اردو (PK)",
        "landing.title": "ٹو ڈو ایپ",
        "landing.subtitle": "فیز II - فل اسٹیک ویب ایپلی کیشن",
        "landing.description": "محفوظ تصدیق اور مستقل اسٹوریج کے ساتھ ایک جدید ، ملٹی یوزر ٹو ڈو ایپلی کیشن۔",
        "landing.secure": "محفوظ",
        "landing.persistent": "مستقل",
        "landing.multiuser": "ملٹی یوزر",
        "landing.getstarted": "شروع کریں",
        "landing.signin": "سائن ان"
    }
};

export function LanguageProvider({ children }: { children: React.ReactNode }) {
    const [language, setLanguage] = useState<Language>("en");

    // Load saved language from localStorage
    useEffect(() => {
        const savedLang = localStorage.getItem("language") as Language;
        if (savedLang && (savedLang === "en" || savedLang === "ur")) {
            setLanguage(savedLang);
        }
    }, []);

    const handleSetLanguage = (lang: Language) => {
        setLanguage(lang);
        localStorage.setItem("language", lang);
    };

    const t = (key: string) => {
        return translations[language][key as keyof typeof translations["en"]] || key;
    };

    return (
        <LanguageContext.Provider value={{ language, setLanguage: handleSetLanguage, t }}>
            {children}
        </LanguageContext.Provider>
    );
}

export function useLanguage() {
    const context = useContext(LanguageContext);
    if (context === undefined) {
        throw new Error("useLanguage must be used within a LanguageProvider");
    }
    return context;
}
