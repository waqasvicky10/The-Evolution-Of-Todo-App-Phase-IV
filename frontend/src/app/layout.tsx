/**
 * Root layout component.
 *
 * Wraps the entire application with providers and global styles.
 * This layout is applied to all pages in the app.
 */

import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/contexts/AuthContext";
import { LanguageProvider } from "@/context/LanguageContext";


const inter = Inter({ subsets: ["latin"] });


export const metadata: Metadata = {
  title: "Todo App - Phase II",
  description: "A modern, multi-user todo application with secure authentication",
};


export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <AuthProvider>
          <LanguageProvider>
            {children}
          </LanguageProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
