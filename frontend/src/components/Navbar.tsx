"use client";

/**
 * Navbar component.
 *
 * Navigation bar for authenticated pages showing app title,
 * user email, and logout button.
 */

import Link from "next/link";
import { useAuth } from "@/contexts/AuthContext";


export default function Navbar() {
  const { user, logout } = useAuth();

  const handleLogout = async () => {
    await logout();
  };

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Left side - App title */}
          <div className="flex items-center">
            <Link href="/dashboard" className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900 hover:text-indigo-600 transition">
                Todo App
              </h1>
            </Link>
          </div>

          {/* Right side - User info and logout */}
          <div className="flex items-center space-x-4">
            {user && (
              <span className="text-sm text-gray-600 hidden sm:inline-block">
                {user.email}
              </span>
            )}
            <button
              onClick={handleLogout}
              className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-md transition duration-150"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}
