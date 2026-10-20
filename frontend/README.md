# SatyaSetu Web Interface (React Client)

Institutional web dashboard for the SatyaSetu Misinformation Intelligence Engine.

## Tech Stack
- **Framework**: React 19 + Vite
- **Icons**: Lucide React
- **Styling**: Tailored CSS tokens & responsive dark mode layout
- **API Client**: Axios

## Development Setup

```bash
# Install dependencies
npm install

# Start local Vite development server
npm run dev
```

By default, the Vite dev server runs at `http://localhost:5173` and proxies requests to the FastAPI backend running on `http://127.0.0.1:8000`.

## Production Build

```bash
npm run build
```

The optimized static assets will be emitted to `dist/`.
