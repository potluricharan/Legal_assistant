// This grabs the Render URL from Vercel's environment variables. 
// If working locally, it falls back to localhost:10000.
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:10000";

export const pingServer = async () => {
    try {
        const response = await fetch(`${BACKEND_URL}/api/test`);
        return await response.json();
    } catch (error) {
        return { message: "❌ Connection failed. Check CORS or your VITE_BACKEND_URL." };
    }
};

export const fetchMockLawyer = async () => {
    try {
        const response = await fetch(`${BACKEND_URL}/api/mock/lawyer`);
        return await response.json();
    } catch (error) {
        return { error: "❌ Failed to fetch data from the backend." };
    }
};