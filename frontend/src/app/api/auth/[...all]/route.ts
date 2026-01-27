/**
 * Better Auth API route handler.
 *
 * This route handles all Better Auth API requests (login, register, logout, etc.)
 * It's the catch-all route for /api/auth/* endpoints.
 */

import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { GET, POST } = toNextJsHandler(auth);
