/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
  // Optional: Configure DaisyUI options
  daisyui: {
    themes: ["light", "dark", "cupcake"], // Add themes you want to use
  },
}
