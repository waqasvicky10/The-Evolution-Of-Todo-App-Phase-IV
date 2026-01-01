# Todo Frontend - Phase II

Next.js frontend for the Todo application with TypeScript, authentication, and task management.

## Tech Stack

- Next.js 14+ (App Router)
- TypeScript 5+
- React 18
- Axios for API calls
- Jest + React Testing Library

## Getting Started

### Prerequisites

- Node.js 18+ and npm

### Installation

```bash
# Install dependencies
npm install

# Copy environment variables
cp .env.local.example .env.local

# Edit .env.local and set your API URL
# NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### Development

```bash
# Start development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build

```bash
# Build for production
npm run build

# Start production server
npm start
```

## Testing

```bash
# Run tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage
```

## Code Quality

```bash
# Lint code
npm run lint

# Format code with Prettier
npm run format
```

## Project Structure

```
src/
├── app/              # Next.js App Router pages
├── components/       # Reusable UI components
├── contexts/         # React Context providers
├── hooks/            # Custom React hooks
├── lib/              # Utility libraries (API client, auth)
├── types/            # TypeScript type definitions
└── utils/            # Helper functions (validation)
```

## Environment Variables

- `NEXT_PUBLIC_API_BASE_URL` - Backend API URL (default: http://localhost:8000)
